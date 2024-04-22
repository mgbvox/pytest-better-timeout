"""...and where to find them."""


import functools
from typing import Callable, Any, Optional, Union, TypeVar


FnIn = TypeVar("FnIn")
FnOut = TypeVar("FnOut")


def trace(
    fn_or_arg: Optional[Union[Callable[[FnIn], FnOut], Any]] = None, *args, **config
):
    """so many nested fns"""
    if (not fn_or_arg) or (not callable(fn_or_arg)):

        @functools.wraps(trace)
        def _config_wrapper(_fn):
            return trace(_fn, *args, **config)

        return _config_wrapper

    else:

        @functools.wraps(fn_or_arg)
        def _tracer(*args, **kwargs):
            print(f"Trace: {args, kwargs}")
            print(f"config: {config}")
            print(f"config args: {args}")
            return fn_or_arg(*args, **kwargs)

        return _tracer


@trace(56)
def foo(x: int):
    """woah so awesome Im a doc, phd"""
    print(x)


@trace
def bar(y):
    """bar, but okay for minors"""
    print(y)


@trace(56, yooooo="wooooo")
def baz(z):
    """Luhrman"""
    print(z)


def main():
    foo(456)
    print(foo.__doc__)
    bar(789)
    print(bar.__doc__)
    baz(3_456_789)
    print(baz.__doc__)


if __name__ == "__main__":
    main()
