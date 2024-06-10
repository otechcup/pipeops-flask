#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bite Express App


__author__ = "PhoenixITng"
__copyright__ = "Copyright 2023 - datetime.utcnow().year, {}".format(__author__)
__credits__ = ["Mr. O"]
__version__ = "os.environ.get('BITE_EXPRESS_VERSION')"
__maintainer__ = __author__
__email__ = "support@bitexpress.ng"
__status__ = "os.environ.get('BITE_EXPRESS_ENVIRONMENT_STATUS')"


# import modules
from flask_restx import fields


class NullableString(fields.String):
    __schema_type__ = ["string", "null"]
    
    
# define database models for api

# # for vendor
# vendor_menu_model = api.model(
#     "Bite Vendor Menu",
#     {
#         'id': fields.Integer(),
#         'status': fields.String(validate=Length(min=2, max=13)),
#         'bite_id': fields.String(validate=Length(max=14)),
#         'bitem_id': fields.String(validate=Length(max=14)),
#         'bitem': fields.String(validate=Length(min=2, max=20)),
#         'image': fields.String(validate=Length(min=2, max=24)),
#         'description': fields.String(validate=Length(min=2, max=100)),
#         'category': fields.String(validate=Length(min=2, max=100)),
#         'price': fields.Float(format="%.2f"),
#         'average_prep_time': fields.Integer(),
#         'date_added': fields.DateTime(),
#         'date_updated': fields.DateTime(),
#     },
# )

# vendor_model = api.model(
#     "Bite Vendor",
#     {
#         'id': fields.Integer(),
#         'bite_id': fields.String(validate=Length(max=14)),
#         'kitchen_name': fields.String(validate=Length(min=2, max=200)),
#         'website_url': fields.String(validate=Length(min=2)),
#         'logo': fields.String(validate=Length(min=2, max=23)),
#         'bio': fields.String(validate=Length(min=2, max=200)),
#         'opening_hour': fields.String(validate=Length(min=2, max=5)),
#         'closing_hour': fields.String(validate=Length(min=2, max=5)),
#         'rating': fields.Float(format="%.1f"),
#         'date_created': fields.DateTime(),
#         'date_updated': fields.DateTime(),
#         'location': fields.Nested(location_model),
#         'menu': fields.Nested(vendor_menu_model),
#     },
# )
