from gimme_cached_property import cached_property


class BaseFunction(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError  # pragma: no cover

    @cached_property
    def _invert(self):
        return InvertFunction(self)

    def __invert__(self):
        return self._invert

    def __and__(self, other):
        return AndFunction(self, other)

    def __or__(self, other):
        return OrFunction(self, other)


class InvertFunction(BaseFunction):
    def __init__(self, original):
        self.__original = original

    def __call__(self, *args, **kwargs):
        return not self.__original(*args, **kwargs)

    @property
    def _invert(self):
        return self.__original


class AndFunction(BaseFunction):
    def __init__(self, a, b):
        self.__a = a
        self.__b = b

    def __call__(self, *args, **kwargs):
        return self.__a(*args, **kwargs) and self.__b(*args, **kwargs)


class OrFunction(BaseFunction):
    def __init__(self, a, b):
        self.__a = a
        self.__b = b

    def __call__(self, *args, **kwargs):
        return self.__a(*args, **kwargs) or self.__b(*args, **kwargs)


class Function(BaseFunction):
    def __init__(self, func):
        self.__func = func

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)
