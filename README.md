# `pylob` | Python Limit-Order-Book
**Fast &amp; minimalist fixed decimal precision limit-order-book (LOB) implementation in pure Python.**

*Package currently in development, bugs are expected.*

The goal is to build an efficient, clean and easy to use package for whoever needs a limit-order-book in their project. 

We aim to keep the API minimalist and simple, while having reasonable performances (for a pure Python implementation). We intend the final project to contain no more than ~1000 lines of code.

<img src="ss.png" width=400>

We implement three types of orders: *FOK*, *GTC* and *GTD*. Every order is defined as a limit order, but will be executed as a market order if its price matches the best (bid or ask) limit price in the book.

For GTD orders, the book only supports whole seconds for the order expiry (order can not expire in 3.8 seconds, will be rounded to 4). 

# Usage

This book runs at a fixed decimal precision through the Python `decimal` package. The precision can be set via the `PYLOB_DECIMAL_PRECISION` environment variable, it's default value being 2.

To be able to use this project, clone the repository and install the requirements: 
```bash
git clone git@github.com:mrochk/pylob.git
cd pylob
pip install -r requirements.txt
```

To run tests, use `make test` or `python3 -m unittest discover test`.

***Placing an order***
```python
import time
import pylob as lob

book = lob.OrderBook('My Order-Book')
book.start()

order_params = lob.OrderParams(
    side=lob.OrderSide.BID,
    price=123.32, # by default runs at 2 digits decimal precision
    quantity=3.4,
    otype=lob.OrderType.GTD, # good-till-date order
    expiry=time.time() + 120 # expires in two minutes
)

# -> at this point an exception will be raised if invalid attributes are provided

result = book(order_params) # let the book process the order

assert result.success() # result object can be used to see various infos about the order execution

order_id = result.order_id() # unique id is used to query our order after it's been placed
status, quantity_left = book.get_order_status(order_id)
print(f'Current status of the order: {status}, quantity left: {quantity_left}.')

print(book.view()) # pretty-print the book
```

***

*Lines count:*
```
   92 pylob/engine/engine.py
    1 pylob/engine/__init__.py
   18 pylob/utils/utils.py
    1 pylob/utils/__init__.py
   64 pylob/order/params.py
    1 pylob/order/__init__.py
  161 pylob/order/order.py
   52 pylob/enums/enums.py
    1 pylob/enums/__init__.py
   64 pylob/orderbook/result.py
  361 pylob/orderbook/orderbook.py
    1 pylob/orderbook/__init__.py
   19 pylob/consts/consts.py
    1 pylob/consts/__init__.py
  137 pylob/limit/limit.py
    1 pylob/limit/__init__.py
  156 pylob/side/side.py
    1 pylob/side/__init__.py
    4 pylob/__init__.py
 1136 total
```

***

# TODOs:

As mentioned earlier, this package is still in early development, and contributions are more than welcome.

The main tasks that have to be done are:
- **More and better testing for edge cases. In fact, some tests have to be rewritten too.**
- **Benchmarking / profiling to have an idea of the performance, and see where it's slow.**
- **Some parts probably need to be rewritten in a cleaner way.**
- **Publish package.**