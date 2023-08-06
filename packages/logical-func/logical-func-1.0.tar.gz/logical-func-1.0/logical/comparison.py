from ._base import (
    BaseFunction as _BaseFunction,
)


class Is(_BaseFunction):
    def __init__(self, val):
        self.__val = val

    def __call__(self, obj):
        return obj is self.__val


class Equal(_BaseFunction):
    def __init__(self, val):
        self.__val = val

    def __call__(self, obj):
        return obj == self.__val


class NotEqual(_BaseFunction):
    def __init__(self, val):
        self.__val = val

    def __call__(self, obj):
        return obj != self.__val


class GreaterThan(_BaseFunction):
    def __init__(self, val):
        self.__val = val

    def __call__(self, obj):
        return obj > self.__val


class LessThan(_BaseFunction):
    def __init__(self, val):
        self.__val = val

    def __call__(self, obj):
        return obj < self.__val


class GreaterThanOrEqual(_BaseFunction):
    def __init__(self, val):
        self.__val = val

    def __call__(self, obj):
        return obj >= self.__val


class LessThanOrEqual(_BaseFunction):
    def __init__(self, val):
        self.__val = val

    def __call__(self, obj):
        return obj <= self.__val
