from ._base import (
    BaseFunction as _BaseFunction,
)


class IsInstance(_BaseFunction):
    def __init__(self, type):
        self.__type = type

    def __call__(self, item):
        return isinstance(item, self.__type)


is_bool = IsInstance(bool)
is_int = IsInstance(int)
is_float = IsInstance(float)
is_str = IsInstance(str)
is_bytes = IsInstance(bytes)

is_num = is_int | is_float
is_any_str = is_str | is_bytes
