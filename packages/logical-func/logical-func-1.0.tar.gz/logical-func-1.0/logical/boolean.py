from ._base import (
    Function as _Function,
)
from .comparison import (
    Is as _Is,
)

true = _Function(lambda *args, **kwargs: True)
false = ~true

is_true = _Is(True)
is_false = _Is(False)

eval_true = _Function(bool)
eval_false = ~eval_true
