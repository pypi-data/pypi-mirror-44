=============================
Python API client for Jet.com
=============================

.. image:: https://badge.fury.io/py/jet-python.png
    :target: http://badge.fury.io/py/jet-python

.. image:: https://travis-ci.org/fulfilio/jet-python.png?branch=master
    :target: https://travis-ci.org/fulfilio/jet-python

Python Jet.com API Client

Installation
------------

.. code-block::

    pip install jet-python



Usage
-----

Get an authenticated jet client
```````````````````````````````

.. code-block:: python

    from jet import Jet
    jet = Jet(
        user='0CXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        secret='NXXXXXXXXXXXXXXXXXXXXXXXXj+',
        merchant_id='d4fe23456789876545678656787652',
    )

Fetch 10 products at a time
```````````````````````````

.. code-block:: python

  skus = jet.products.get_skus(page=1)


Find ready to ship orders
```````````````````````````

.. code-block:: python

    order_ids = jet.orders.get_recent_order_ids(
        status='ready'
    )


Acknowledge an order
```````````````````````````

.. code-block:: python

    jet.orders.acknowledge(order_id)


Mark an order as shipped
````````````````````````

This involved a nested data structure. To make this easier
this module provides a convenient higher level data
structure called `jet.Shipment`

.. code-block:: python


    from jet import Shipment

    shipment = Shipment(
        shipment_id='CS1234',
        tracking_number='1Z12324X12342435',
        ship_from_zip_code='91789',
        shipment_date=date.today(),
        carrier='UPS',
        shipment_method='Other'
    )

    for item in items:
        shipment.add_item(
            sku='iphone-xs',
            quantity=2,
        )

    jet.orders.ship(order_id, [shipment])


Features
--------

* TODO

