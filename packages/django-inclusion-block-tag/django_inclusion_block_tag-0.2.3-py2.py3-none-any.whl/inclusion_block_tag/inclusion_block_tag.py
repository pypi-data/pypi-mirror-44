import functools
from copy import copy
from inspect import getfullargspec

from django.template.library import TagHelperNode, parse_bits
from django.template.loader import get_template


class InclusionBlockNode(TagHelperNode):
    """Add kwargs to context node and render nodelist.
    """

    def __init__(self, func, takes_context, args, kwargs, nodelist, filename):
        super().__init__(func, takes_context, args, kwargs)
        self.nodelist = nodelist
        self.filename = filename

    def render(self, context):
        new_context = copy(context)
        resolved_args, resolved_kwargs = self.get_resolved_arguments(context)
        _dict = self.func(*resolved_args, **resolved_kwargs)
        new_context.update(_dict)

        # render inner with context
        content = self.nodelist.render(new_context)

        new_context['content'] = content
        t = get_template(self.filename)
        return t.render(new_context.flatten())


def inclusion_block_tag(register, filename, func=None, takes_context=None, name=None):
    """
    """

    def dec(func):
        params, varargs, varkw, defaults, kwonly, kwonly_defaults, _ = getfullargspec(
            func
        )
        function_name = name or getattr(func, "_decorated_function", func).__name__

        @functools.wraps(func)
        def compile_func(parser, token):
            bits = token.split_contents()[1:]
            args, kwargs = parse_bits(
                parser,
                bits,
                params,
                varargs,
                varkw,
                defaults,
                kwonly,
                kwonly_defaults,
                takes_context,
                function_name,
            )
            nodelist = parser.parse(("end{}".format(function_name),))
            parser.delete_first_token()
            return InclusionBlockNode(
                func, takes_context, args, kwargs, nodelist, filename
            )

        register.tag(function_name, compile_func)
        return func

    return dec
