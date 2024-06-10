#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BiteExpress App


__author__ = "PhoenixITng"
__copyright__ = f"Copyright 2023 - datetime.utcnow().year, {__author__}"
__credits__ = ["Mr. O"]
__version__ = "config('BITE_EXPRESS_VERSION', cast=float)"
__maintainer__ = __author__
__email__ = "info@biteexpress.ng"
__status__ = "config('BITE_EXPRESS_ENVIRONMENT_STATUS', cast=str)"


# import modules
from flask_restx import fields

from .routes import menu, biteexer, order_history
from bite_express.utils import NullableString


menu_form_model = menu.model(
    "BiteExpress Menu",
    {
        'bitem': fields.String(required=True, min_length=2, max_length=20),
        'status': fields.String(required=True, min_length=2, max_length=13),
        'image': fields.String(required=True, min_length=2, max_length=24),
        'description': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'category': fields.String(required=True, min_length=2, max_length=100),
        'price': fields.Arbitrary(required=True),
        'average_prep_time': fields.String(required=True, min_length=8),
        'offer': NullableString(max_length=20),
    },
)
bitex_vendor_menu_model = menu.inherit(
    "BitexVendor Menu",
    menu_form_model,
    {
        'id': fields.Integer(required=True),
        'kitchen_name': fields.String(
            required=True, min_length=2, max_length=200
        ),
        'bitem_id': fields.String(required=True, max_length=14),
        'quantity': fields.Integer(required=True),
        'liked_by': fields.List(fields.String(), required=True),
        'viewed_by': fields.List(fields.String(), required=True),
        'date_added': fields.DateTime(required=True),
        'date_updated': fields.DateTime(required=True),
    },
)
account_privilege_model = biteexer.model(
    "BiteExer Privilege",
    {
        'id': fields.Integer(required=True),
        'status': fields.String(required=True, min_length=2, max_length=100),
        'role': fields.String(required=True, min_length=2, max_length=8),
        'title': fields.String(required=True, min_length=2, max_length=300),
        'permission': fields.List(fields.String(), required=True),
        'date_assigned': fields.DateTime(required=True),
        'date_updated': fields.DateTime(required=True),
    },
)
basic_info_model = biteexer.model(
    "BiteExer Basic Information",
    {
        'id': fields.Integer(required=True),
        'username': fields.String(required=True, min_length=2, max_length=100),
        'profile_picture': fields.String(
            required=True, min_length=2, max_length=20
        ),
        'gender': fields.String(required=True, min_length=2, max_length=6),
        'birthday': fields.Date(required=True),
        'phone_number': fields.Integer(required=True),
        'email_address': fields.String(
            required=True, min_length=2, max_length=500
        ),
        'date_updated': fields.DateTime(required=True),
    },
)
location_model = biteexer.model(
    "BiteExer Location",
    {
        'id': fields.Integer(required=True),
        'country': fields.String(required=True, min_length=2, max_length=100),
        'state_region': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'city': fields.String(required=True, min_length=2, max_length=100),
        'neighbourhood': fields.String(
            required=True, min_length=2, max_length=200
        ),
        'post_code': fields.Integer(required=True),
        'date_added': fields.DateTime(required=True),
        'date_updated': fields.DateTime(required=True),
    },
)
credit_card_model = biteexer.model(
    "BiteExer Credit Card",
    {
        'id': fields.Integer(required=True),
        'bank_name': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'account_name': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'account_number': fields.Integer(required=True),
        'card_name': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'card_number': fields.Integer(required=True),
        'card_expiration_date': fields.Date(required=True),
        'cvv': fields.Integer(required=True),
        'date_added': fields.DateTime(required=True),
        'date_updated': fields.DateTime(required=True),
    },
)
wallet_model = biteexer.model(
    "BiteExer Wallet",
    {
        'id': fields.Integer(required=True),
        'wallet_balance': fields.Arbitrary(required=True),
        'deposit': fields.Arbitrary(required=True),
        'referral': fields.Integer(required=True),
        'total_earning': fields.Arbitrary(required=True),
        'fund_transfer': fields.Arbitrary(required=True),
        'pending_payout': fields.Arbitrary(required=True),
        'payout': fields.Arbitrary(required=True),
        'date_updated': fields.DateTime(required=True),
    },
)

biteexpress_order_history_form_model = order_history.model(
    "BiteExpress Order History Form",
    {
        'bitem_id': fields.String(required=True, min_length=2, max_length=20),
        'price': fields.Arbitrary(required=True),
        'quantity': fields.Integer(required=True),
        'destination': fields.String(
            required=True, min_length=2, max_length=200
        ),
    },
)
order_history_form_model = order_history.model(
    "BiteExpress Order History",
    {
        'order_history': fields.List(
            fields.Nested(biteexpress_order_history_form_model), required=True
        ),
    },
)
order_history_model = order_history.inherit(
    "BitexUser-BitexAgent Order History",
    biteexpress_order_history_form_model,
    {
        'id': fields.Integer(required=True),
        'status': fields.String(required=True, min_length=2, max_length=8),
        'prep_time': fields.Integer(required=True),
        'driver': fields.String(required=True, max_length=14),
        'delivery_time': fields.Integer(required=True),
        'delivered': fields.Boolean(required=True),
        'received': fields.Boolean(required=True),
        'returned': fields.Boolean(required=True),
        'date_ordered': fields.DateTime(required=True),
        'date_updated': fields.DateTime(required=True),
    },
)
transaction_history_model = biteexer.model(
    "BiteExer Transaction History",
    {
        'id': fields.Integer(required=True),
        'type': fields.String(required=True, min_length=2, max_length=7),
        'amount': fields.Arbitrary(required=True),
        'hash': fields.String(required=True, min_length=2, max_length=18),
        'status': fields.String(required=True, min_length=2, max_length=9),
        'date_created': fields.DateTime(required=True),
        'confirmed_by': fields.String(required=True, max_length=14),
        'date_confirmed': fields.DateTime(required=True),
        'date_updated': fields.DateTime(required=True),
    },
)
biteexer_model = biteexer.model(
    "BiteExer Profile Information",
    {
        'id': fields.Integer(required=True),
        'referrer_id': fields.String(required=True, max_length=15),
        'kitchen_id': fields.String(required=True, max_length=15),
        'bite_id': fields.String(required=True, max_length=15),
        'account_status': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'first_name': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'middle_name': fields.String(required=True, max_length=100),
        'last_name': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'last_seen': fields.DateTime(required=True),
        'date_created': fields.DateTime(required=True),
        'date_updated': fields.DateTime(required=True),
        'privilege': fields.Nested(
            account_privilege_model, required=True
        ),
        'basic_info': fields.Nested(basic_info_model, required=True),
        'location': fields.Nested(location_model, required=True),
        'credit_card': fields.List(
            fields.Nested(credit_card_model), required=True
        ),
        'wallet': fields.Nested(wallet_model, required=True),
        'order_history': fields.List(
            fields.Nested(order_history_model), required=True
        ),
        'transaction_history': fields.List(
            fields.Nested(transaction_history_model), required=True
        ),
    },
)
