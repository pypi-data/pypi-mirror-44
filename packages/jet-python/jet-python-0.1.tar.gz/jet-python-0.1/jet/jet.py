# -*- coding: utf-8 -*-
import requests
from dateutil.parser import parse as parse_date


class Jet(object):
    """
    Jet.com API Client
    """

    base_url = "https://merchant-api.jet.com/api"

    def __init__(self, user, secret, merchant_id):
        self.user = user
        self.secret = secret
        self.merchant_id = merchant_id
        self.token = None
        self.token_expires_on = None
        self.get_token()

    def get_token(self):
        token_data = requests.post(
            self.base_url + '/token',
            json={
                'user': self.user,
                'pass': self.secret,
            }
        ).json()
        self.token = token_data['id_token']
        self.token_expires_on = parse_date(
            token_data['expires_on']
        )
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'bearer %s' % (
            self.token
        )

    @property
    def products(self):
        return Product(self)

    @property
    def orders(self):
        return Order(self)


class Product(object):
    """
    The Products API is used to perform specific actions
    to a single product and is good for isolated changes.

    For retailers with large catalogs, use the Catalog API
    """
    def __init__(self, client):
        self.client = client

    def update_price(self, sku, price):
        """
        At Jet, the price the retailer sets is not the same as the price
        the customer pays. The price set for a SKU will be the price the
        retailer gets paid for selling the products. However, the price
        that is set will influence how competitive your product offer
        matches up compared to other product offers for the same SKU.

        TODO: Implement support for fulfillment nodes

        https://developer.jet.com/docs/merchant-sku-price
        """
        return self.client.session.post(
            self.client.base_url + '/merchant-skus/' + sku,
            json={'price': price}
        ).json()

    def get_sku(self, sku):
        """
        Retrieve information about SKUs
        """
        return self.client.session.get(
            self.client.base_url + '/merchant-skus/' + sku,
        ).json()

    def get_price(self, sku):
        """
        Retrieve price information of SKU
        """
        return self.client.session.get(
            self.client.base_url + '/merchant-skus/' + sku + '/price',
        ).json()

    def get_inventory(self, sku):
        """
        Retrieve inventory information of SKU
        """
        return self.client.session.get(
            self.client.base_url + '/merchant-skus/' + sku + '/inventory',
        ).json()

    def get_skus(self, page=1, per_page=10):
        """
        Retrieve multiple SKUs at once
        """
        urls = self.client.session.get(
            self.client.base_url + '/merchant-skus',
            params={
                "offset": (page - 1) * per_page,
                "limit": per_page,
            }
        ).json()['sku_urls']
        return [
            self.get_sku(url.rsplit('/')[-1])
            for url in urls
        ]


class Order(object):
    """

    """

    def __init__(self, client):
        self.client = client

    def get_recent_order_ids(self, status, cancelled=None, fulfillment_node=None):
        """
        Access the first 1000 orders in a certain status. Orders will only
        be available by status for 90 days after order creation.

        Status can be one of the following:

        * 'created' -       The order has just been placed. Jet.com allows a
                            half hour for fraud check and customer cancellation.
                            Retailers NOT fulfill orders that are created.
        * 'ready' -         The order is ready to be fulfilled by the retailer
        * 'acknowledged'    The order has been accepted by the retailer and
                            is awaiting fulfillment
        * 'inprogress' -    The order is partially shipped
        * 'complete' -      The order is completely shipped or cancelled. All units have
                            been accounted for

        Returns a list of recent order ids
        """
        params = {}

        if cancelled is not None:
            params['isCancelled'] = 'true' if cancelled else 'false'

        if fulfillment_node:
            params['fulfillment_node'] = fulfillment_node

        order_urls = self.client.session.get(
            self.client.base_url + '/orders/%s' % status,
            params=params
        ).json()['order_urls']
        return [
            url.rsplit('/')[-1] for url in order_urls
        ]

    def get_order(self, order_id):
        """
        Retreive an order with the given ID
        """
        return self.client.session.get(
            self.client.base_url + '/orders/withoutShipmentDetail/%s' % order_id,
        ).json()

    def acknowledge(self, order_id, status='accepted',
                    alt_order_id=None, order_items=None):
        """
        The order acknowledge call is utilized to allow a retailer to accept or
        reject an order. If there are any skus in the order that cannot be
        fulfilled then you will reject the order.

        Valid statuses are:

        * rejected - other
        * rejected - fraud
        * rejected - item level error
        * rejected - ship from location not available
        * rejected - shipping method not supported
        * rejected - unfulfillable address
        * accepted

        :param alt_order_id: Option merchant supplied order ID.
        :param order_items: See https://developer.jet.com/docs/acknowledge-order
        """
        body = {
            'acknowledgement_status': status,
        }
        if alt_order_id is not None:
            body['alt_order_id'] = alt_order_id
        if order_items is not None:
            body['order_items'] = order_items
        return self.client.session.put(
            self.client.base_url + '/orders/%s/acknowledge' % order_id,
            json=body
        ).json()

    def ship(self, order_id, shipments):
        """
        The order shipped call is utilized to provide Jet with the SKUs
        that have been shipped or cancelled in an order, the tracking information,
        carrier information and any additional returns information for the order.
        """
        body = {"shipments": []}
        for shipment in shipments:
            if isinstance(shipment, Shipment):
                body['shipments'].append(shipment.to_dict())
            else:
                body['shipments'].append(shipment)
        return self.client.session.put(
            self.client.base_url + '/orders/%s/ship' % order_id,
            json=body
        ).json()


class Shipment(object):
    """
    A shipment object corresponding to an order.

    For carrier codes and shipment methods, refer the link
    below:

    https://developer.jet.com/docs/ship-order
    """

    def __init__(self, shipment_id, tracking_number,
                 ship_from_zip_code,
                 shipment_date=None,
                 expected_delivery_date=None,
                 shipment_method='Other',
                 carrier='Other',
                 pick_up_date=None,
                 ):
        self.shipment_id = shipment_id
        self.ship_from_zip_code = ship_from_zip_code
        self.tracking_number = tracking_number
        self.shipment_date = shipment_date
        self.expected_delivery_date = expected_delivery_date
        self.shipment_method = shipment_method
        self.carrier = carrier
        self.pick_up_date = pick_up_date

        self.items = []

    def to_dict(self):
        rv = {
            'alt_shipment_id': self.shipment_id,
            'shipment_tracking_number': self.tracking_number,
            'response_shipment_method': self.shipment_method,
            'ship_from_zip_code': self.ship_from_zip_code,
            'carrier': self.carrier,
            'shipment_items': self.items,
        }
        if self.shipment_date:
            rv['response_shipment_date'] = self.shipment_date.isoformat()
        if self.expected_delivery_date:
            rv['expected_delivery_date'] = self.expected_delivery_date.isoformat()
        if self.pick_up_date:
            rv['carrier_pick_up_date'] = self.pick_up_date.isoformat()

    def add_item(self, sku, quantity, cancel_quantity=None):
        """
        Add an item to the shipment
        """
        rv = {
            'merchant_sku': sku,
            'response_shipment_sku_quantity': quantity,
        }

        if cancel_quantity is not None:
            rv['response_shipment_cancel_qty'] = cancel_quantity

        self.items.append(rv)
