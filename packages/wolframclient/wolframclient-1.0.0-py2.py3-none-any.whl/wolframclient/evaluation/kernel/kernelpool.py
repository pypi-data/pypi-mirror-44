# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import logging
import itertools
from asyncio import CancelledError


from wolframclient.evaluation.kernel.asyncsession import (
    WolframLanguageAsyncSession)
from wolframclient.exception import WolframKernelException
from wolframclient.evaluation.base import WolframAsyncEvaluator
from wolframclient.utils.six import iterable_types, string_types
from wolframclient.utils.functional import is_iterable
from wolframclient.utils.api import asyncio

logger = logging.getLogger(__name__)

__all__ = ['WolframKernelPool', 'parallel_evaluate']


class WolframKernelPool(WolframAsyncEvaluator):
    """ A pool of kernels to dispatch one-shot evaluations asynchronously.

    Kernel can be specified in various ways. A string representing the path to a local kernel and used to
    instanciante an instance of :class:`wolframclient.evaluation.WolframLanguageAsyncSession`, a :class:`wolframclient.evaluation.WolframCloudAsyncSession`,
    an instance of :class:`wolframclient.evaluation.WolframLanguageAsyncSession`. It is also possible to provide an iterable object yielding those specifications.
    If the number of element is less than the requested pool size (`poolsize`), the element are duplicated until the requested size is reached.

    `poolsize` is the number of kernel instances. Beware of licencing limits and choose this parameter accordingly.
    `load_factor` indicate how many workloads are queued per kernel before put operation blocks. Values below or equal to 0 means infinite queue size.
    `loop` event loop to use.
    `kwargs` are passed to :class:`wolframclient.evaluation.WolframLanguageAsyncSession` during initialization.
    """

    def __init__(self,
                 async_evaluators,
                 poolsize=4,
                 load_factor=0,
                 loop=None,
                 async_language_session_class=WolframLanguageAsyncSession,
                 **kwargs):
        super().__init__(loop)
        if poolsize <= 0:
            raise ValueError(
                'Invalid pool size value %i. Expecting a positive integer.' %
                i)
        self._queue = asyncio.Queue(load_factor * poolsize, loop=self._loop)
        self.async_language_session_class = async_language_session_class
        self._evaluators = set()
        if isinstance(async_evaluators, string_types):
            for _ in range(poolsize):
                self._add_evaluator(async_evaluators, **kwargs)
        else:
            if not is_iterable(async_evaluators):
                async_evaluators = itertools.repeat(async_evaluators)
            for evaluator in itertools.cycle(async_evaluators):
                if len(self._evaluators) >= poolsize:
                    break
                self._add_evaluator(evaluator)
            
        self._started_tasks = []
        self._pending_init_tasks = None
        self.last = 0
        self.eval_count = 0
        self.requestedsize = poolsize        

    def _add_evaluator(self, evaluator, **kwargs):
        if isinstance(evaluator, string_types):
            self._evaluators.add(self.async_language_session_class(evaluator, loop=self._loop, **kwargs))
        elif isinstance(evaluator, WolframAsyncEvaluator):
            if evaluator in self._evaluators:
                self._evaluators.add(evaluator.duplicate())
            else:
                self._evaluators.add(evaluator)
        else:
            raise ValueError('Invalid asynchronous evaluator specifications. %s is neither a string nor a WolframAsyncEvaluator instance.' % evaluator)

    async def _kernel_loop(self, kernel):
        while True:
            try:
                future = None
                task = None
                logger.debug('Wait for a new queue entry.')
                task = await self._queue.get()
                if task is None:
                    logger.info(
                        'Termination requested for kernel: %s.' % kernel)
                    break
                # func is one of the evaluate* methods from WolframAsyncEvaluator.
                future, func, args, kwargs = task
                # those method can't be canceled since the kernel is evaluating anyway.
                try:
                    func = getattr(kernel, func)
                    result = await asyncio.shield(
                        func(*args, **kwargs))
                    future.set_result(result)
                except Exception as e:
                    future.set_exception(e)
            # First exceptions are those we can't recover from.
            except KeyboardInterrupt as interrupt:
                logger.error(
                    'Loop associated to kernel %s interrupted by user.',
                    kernel)
                raise interrupt
            except CancelledError as cancel:
                logger.warning('Loop associated to kernel %s cancelled.',
                               kernel)
                raise cancel
            except RuntimeError as runtime:
                logger.error('Unexpected runtime error: {}', runtime)
                raise runtime
            except Exception as e:
                if future:
                    logger.warning(
                        'Exception raised in loop returned in future object. Exception was: %s'
                        % e)
                    future.set_exception(e)
                else:
                    logger.warning(
                        'No future object. Exception raised in loop was: %s' %
                        e)
                    raise e
            finally:
                if task:
                    self._queue.task_done()

    async def _async_start_kernel(self, kernel):
        kernel_started = False
        try:
            # start the kernel
            await kernel.start()
            kernel_started = True
        except asyncio.CancelledError:
            logger.info('Cancelled signal during kernel start.')
        except Exception as e:
            try:
                if logger.isEnabledFor(logging.INFO):
                    logger.info(
                        'A kernel from pool failed to start: %s. Reason is %s',
                        kernel, e)
                await kernel.stop()
            except asyncio.CancelledError:
                logger.info('Cancelled signal.')
            except Exception as e2:
                logger.info(
                    'Exception raised during clean-up after failed start: %s',
                    e2)

        if kernel_started:
            # shedule the infinite evaluation loop
            task = asyncio.create_task(
                self._kernel_loop(kernel))
            if logger.isEnabledFor(logging.INFO):
                logger.info('New kernel started in pool: %s.', kernel)
            # register the task. The loop is not always started at this point.
            self._started_tasks.append(task)

    @property
    def started(self):
        return len(self._started_tasks) > 0

    async def start(self):
        """ Start a pool of kernels and wait for at least one of them to 
        be ready for evaluation.

        This method is a coroutine.
        If not all the kernels were able to start fails and terminate the pool.
        """
        self.stopped = False
        # keep track of the init tasks. We have to wait before terminating.
        self._pending_init_tasks = {(asyncio.create_task(
            self._async_start_kernel(kernel)))
                                    for kernel in self._evaluators}
        # uninitialized kernels are removed if they failed to start
        # if they do start the task (the loop) is added to _started_tasks.
        # we need at least one working kernel.
        # we also need to keep track of start kernel tasks in case of early termination.
        while len(self._started_tasks) == 0:
            if len(self._pending_init_tasks) == 0:
                raise WolframKernelException('Failed to start any kernel.')
            _, self._pending_init_tasks = await asyncio.wait(
                self._pending_init_tasks, return_when=asyncio.FIRST_COMPLETED)
        logger.info('Pool initialized with %i running kernels',
                    len(self._started_tasks))

    async def stop(self):
        self.stopped = True
        #  todo cancel with self.event_abort.set() ???

        # make sure all init tasks are finished.
        if len(self._pending_init_tasks) > 0:
            for task in self._pending_init_tasks:
                task.cancel()
            await asyncio.wait(self._pending_init_tasks)
        if len(self._started_tasks) > 0:
            try:
                # request for loop termination.
                for _ in range(len(self._started_tasks)):
                    await self._queue.put(None)
                # wait for loop to finish before terminating the kernels
                await asyncio.wait(self._started_tasks, loop=self._loop)
            except CancelledError:
                pass
            except Exception as e:
                logger.warning('Exception raised while terminating loop: %s',
                               e)
        # terminate the kernel instances, if any started.
        tasks = {
            asyncio.create_task(kernel.stop())
            for kernel in self._evaluators
        }
        # `wait` raises the first exception, but wait for all tasks to finish.
        await asyncio.wait(tasks, loop=self._loop)

    async def terminate(self):
        await self.stop()

    async def _ensure_started(self):
        if not self.started:
            await self.start()
        if self.stopped:
            await self.restart()

    async def _put_evaluation_task(self, future, func, expr, **kwargs):
        await self._ensure_started()
        await self._queue.put((future, func, (expr, ), kwargs))
        self.eval_count += 1

    async def evaluate(self, expr, **kwargs):
        future = asyncio.Future(loop=self._loop)
        await self._put_evaluation_task(
            future, 'evaluate', expr, **kwargs)
        return await future

    async def evaluate_wxf(self, expr, **kwargs):
        future = asyncio.Future(loop=self._loop)
        await self._put_evaluation_task(
            future, 'evaluate_wxf', expr, **kwargs)
        return await future

    async def evaluate_wrap(self, expr, **kwargs):
        future = asyncio.Future(loop=self._loop)
        await self._put_evaluation_task(
            future, 'evaluate_wrap', expr, **kwargs)
        return await future

    def evaluate_all(self, iterable):
        return self._loop.run_until_complete(self._evaluate_all(iterable))

    async def _evaluate_all(self, iterable):
        tasks = [asyncio.create_task(self.evaluate(expr)) for expr in iterable]
        return await asyncio.gather(*tasks)

    def __repr__(self):
        return 'WolframKernelPool<%i/%i started evaluators, cummulating %i evaluations>' % (
            len(self._started_tasks), self.requestedsize, self.eval_count)

    def __len__(self):
        return len(self._started_tasks)


def parallel_evaluate(evaluator_spec, expressions, max_kernels=4, loop=None):
    """ Start a kernel pool using `evaluator_spec` and evaluate the expressions on the created
    pool, then terminate it and returns the results.

    Note that each evaluation should be independent and not rely on any previous one, since
    there is no guarantee that two given expr evaluates on the same kernel, and scoped to 
    avoid side effects.
    """
    loop = loop or asyncio.get_event_loop()
    pool = None
    try:
        pool = WolframKernelPool(evaluator_spec, poolsize=max_kernels, loop=loop)
        loop.run_until_complete(pool.start())
        return pool.evaluate_all(expressions)
    finally:
        if pool:
            loop.run_until_complete(pool.terminate())
