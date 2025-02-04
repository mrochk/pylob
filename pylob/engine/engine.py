'''
The matching engine module, could also be a static class.
'''

from dataclasses import dataclass
from typing import Optional

from pylob import OrderType
from pylob.limit import Limit
from pylob.side import Side
from pylob.order import Order

@dataclass(init=True, repr=True)
class ExecutionResult:
    success        : bool
    identifier     : Optional[int]
    orders_matched : int
    limits_matched : int

def execute(order : Order, side : Side) -> ExecutionResult:
    '''Execute a market order.

    Args:
        order (Order): The order to execute.
        side (Side): The side at which the order should be executed.
    '''
    limits_matched = orders_matched = 0
    
    lim = side.best()

    while order.quantity() >= lim.volume():
        limits_matched += 1
        orders_matched += lim.size()

        order.partial_fill(lim.volume())
        side.remove_limit(lim.price())
        
        lim = side.best()

    lim_order = lim.next_order()

    while order.quantity() > lim_order.quantity():
        orders_matched += 1

        order.partial_fill(lim_order.quantity())
        lim.pop_next_order()
        lim_order = lim.next_order()

    lim.partial_fill(lim_order.id(), order.quantity())

    return ExecutionResult(
        success=True,
        identifier=order.id(),
        orders_matched=orders_matched,
        limits_matched=limits_matched,
    )

def place(order : Order, side : Side):
    '''Place a limit order.

    Args:
        order (Order): The order to place.
        side (Side): The side at which the order should be place.
    '''
    if not side.limit_exists(order.price()):
        side.add_limit(order.price())

    side.add_order(order)