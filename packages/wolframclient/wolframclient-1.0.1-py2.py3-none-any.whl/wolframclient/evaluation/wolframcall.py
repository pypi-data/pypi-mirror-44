# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from wolframclient.exception import WolframLanguageException
from wolframclient.utils.encoding import force_text
from wolframclient.language import wl
from wolframclient.language.expression import WLSymbol

class WolframCall(object):
    def __init__(self, session):
        self.session = session

    def __getattr__(self, attr):
        """Intercept attributes starting with a capital letter and evaluate them as a System symbol.
        """
        if attr[0].isupper():
            functions = attr.split('_')
            if len(functions) > 1:
                def inner(*args, **kwargs):
                    if not self.session.started:
                        raise WolframEvaluationException('Session is not started.')
                    return self.session.evaluate(expr_from_attr(functions, *args, **kwargs))
                return inner
            else:
                return self.session.evaluate(WLSymbol(attr))
        else:
            raise AttributeError('%s object has no attribute %s' %
                                 (self.__class__.__name__, attr))

def expr_from_attr(functions, *args, **options):
    """ Syntactic sugar for System function, apply composition to functions names separated by an underscore.

    E.g: expr_from_attr('Total_Range', 3) is equivalent to Python `wl.Total(wl.Range(3))`, and 
    Wolfram Language `Total[Range[3]]`.

    Convert Python named attributes into Wolfram Language :wl:`Options`.
    """
    if options:
        wl_args = list(args)
        for k, v in options.items():
            if k.endswith('_'):
                wl_args.append(wl.Rule(force_text(k[:-1]), v))
            else:
                wl_args.append(wl.Rule(WLSymbol(k), v))
        expr = WLSymbol(force_text(functions[-1]))(*wl_args)
    else:
        expr = WLSymbol(force_text(functions[-1]))(*args)
    if len(functions) > 1:
        functions = [WLSymbol(x) for x in functions[:-1]]
        expr = wl.Composition(*functions)(expr)
    return expr
