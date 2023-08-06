# logical-func

[![Build Status](https://travis-ci.com/MichaelKim0407/logical-func.svg?branch=master)](https://travis-ci.com/MichaelKim0407/logical-func)
[![Coverage Status](https://coveralls.io/repos/github/MichaelKim0407/logical-func/badge.svg?branch=master)](https://coveralls.io/github/MichaelKim0407/logical-func?branch=master)

Boolean-returning callables with logical operations.

## Usage

```python
fizz = Function(lambda x: x % 3 == 0)
buzz = Function(lambda x: x % 5 == 0)
fizzbuzz = fizz & buzz
not_fizz = ~fizz
fizz_or_buzz = fizz | buzz

fizz(3)  # True
fizz(5)  # False
buzz(5)  # True
fizzbuzz(15)  # True
not_fizz(10)  # True
fizz_or_buzz(6)  # True
```

## Installation

```bash
pip install logical-func
```

## Callables and classes

Classes expects certain arguments in `__init__`
and instances are boolean-callables.

`logical` module

* `class Function`: Wrap a bool-returning function.

`logical.typing` module

* `class IsInstance`
* `is_bool`: is `bool`.
* `is_int`: is `int`.
* `is_float`: is `float`.
* `is_str`: is `str`.
* `is_bytes`: is `bytes`.
* `is_num`: is `int` or `float`.
* `is_any_str`: is `str` or `bytes`.

`logical.boolean` module

* `true`: always returns `True`.
* `false`: always returns `False`.
* `is_true`: is `True`.
* `is_false`: is `False`.
* `eval_true`: `bool` call returns `True`.
* `eval_false`: `bool` call returns `False`.

`logical.num` module

* `is_integer`: is `int` or `float` with integral value (e.g. `1.0`).
* `is_not_integer`: not `is_integer`.
* `class DivBy`
* `is_even`: can be divided by 2.
* `is_odd`: cannot be divided by 2.

`logical.comparison` module

* `class Is`
* `class Equal`
* `class NotEqual`
* `class GreaterThan`
* `class LessThan`
* `class GreaterThanOrEqual`
* `class LessThanOrEqual`

See [tests](tests/) for usage examples.
