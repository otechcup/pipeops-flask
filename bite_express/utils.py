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


class NullableString(fields.String):
    __schema_type__ = ["string", "null"]
    
    
# define database models for api

# # for vendor
# bitex_vendor_menu_model = api.model(
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
#         'menu': fields.Nested(bitex_vendor_menu_model),
#     },
# )



# from bite_express import bcrypt

# def genesis_account():
#   hash_password = bcrypt.generate_password_hash("mr.o.josh@cap.tech").decode("utf-8")
#   biteexer_account = BiteExer(bite_id="00000-BTE-00000", first_name="Mr.", last_name="O")
#   account_privilege = BiteExerAccountPrivilege(bite_id=biteexer_account.bite_id, title="BitexUser", role="BiteExer")
#   basic_info = BiteExerBasicInfo(bite_id=biteexer_account.bite_id, phone_number="+2347053001118", email_address="mrojosh.cap.tech@gmail.com")
#   secure_account = BiteExerAccountSecurity(bite_id=biteexer_account.bite_id, password_hash=hash_password)
#   wallet = BiteExerWallet(bite_id=biteexer_account.bite_id)

#   biteexer_account.add()
#   account_privilege.add()
#   basic_info.add()
#   secure_account.add()
#   wallet.add()
