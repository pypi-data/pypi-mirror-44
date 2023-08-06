try:
    from ._base import Function
except ImportError:  # pragma: no cover
    # setup.py imports __version__, at which point dependencies in _base may not be installed
    pass

__version__ = '1.0'
