from ._base import (
    BaseFunction as _BaseFunction,
    Function as _Function,
)
from .typing import (
    is_int as _is_int,
)

is_integer = _is_int | _Function(lambda x: x == int(x))
is_not_integer = ~is_integer


class DivBy(_BaseFunction):
    def __init__(self, n):
        self.__n = n

    def __call__(self, x):
        return x % self.__n == 0


is_even = DivBy(2)
is_odd = ~is_even
