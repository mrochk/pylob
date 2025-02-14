import os
from decimal import Decimal

DECIMAL_PRECISION_ENV_VARNAME: str = 'PYLOB_DECIMAL_PRECISION'

DEFAULT_DECIMAL_PRECISION: int = 2

def get_precision() -> int:
    precision = os.environ.get(DECIMAL_PRECISION_ENV_VARNAME)
    return int(precision) if precision else DEFAULT_DECIMAL_PRECISION

DECIMAL_PRECISION: int = get_precision()

MIN_VALUE = UNIT = Decimal('0.' + ('0' * (DECIMAL_PRECISION - 1)) + '1')

MAX_VALUE = Decimal(int(10e10))

ORDERS_ID_SIZE = 8

def zero(): return Decimal('0')
