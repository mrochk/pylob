from decimal import Decimal
from collections import deque
from typing import Optional

from pylob import todecimal
from pylob.order import Order
from pylob.consts import num

class Limit:
    '''
    A limit is a collection of orders.
    '''
    price    : Decimal
    volume   : Decimal
    orderq   : deque[Order]
    ordermap : dict[Order]

    def __init__(self, price : num):
        self.price = todecimal(price)
        self.volume = Decimal(0)
        self.orderq = deque()
        self.ordermap = dict()

    def add_order(self, order : Order) -> bool:
        # do not add order if qty <= 0
        if order.quantity <= 0: return False

        # do not add order is price is different
        if self.price != order.price: return False

        # do not add same order two times
        if order.identifier in self.ordermap.keys(): return False

        # add order
        self.ordermap[order.identifier] = order
        self.orderq.append(order)

        # add volume
        self.volume = self.volume + order.quantity

        return True

    def get_order(self, identifier : int) -> Optional[Order]:
        if identifier in self.ordermap: return self.ordermap[identifier]
        return None

    def execute(self, order : Order) -> bool:
        assert order.quantity <= self.volume

        to_fill = order.quantity
        first_order : Order = self.orderq[0]

        if first_order.quantity > to_fill:
            first_order.quantity -= to_fill
            self.volume -= to_fill
            to_fill = 0
            return True

        if first_order.quantity == to_fill:
            self.volume -= first_order.quantity
            self.orderq.popleft()
            to_fill = 0
            return True

        # is greater

        self.volume -= first_order.quantity
        order.quantity -= first_order.quantity
        self.orderq.popleft()

        return self.execute(order)

    def size(self) -> int: return len(self.orderq)

    def display_orders(self) -> None: print(self.orderq)

    def sanity_check(self) -> bool:
        '''
        Check if price correct for all orders, 
        no duplicates and all of same type.
        '''
        side = self.orderq[0].side 

        for order in self.orderq:
            if order.price != self.price: return False
            if order.side != side: return False

        return True

    def __repr__(self) -> str:
        p = self.price
        size = len(self.orderq)
        volume = self.volume
        return f'Limit(price={p}, size={size}, vol={volume})'