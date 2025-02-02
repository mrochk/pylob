from decimal import Decimal
from numbers import Number
from typing import Union

num = Union[Number | Decimal] # helper typing constant

DEFAULT_DECIMAL_PRECISION = 2