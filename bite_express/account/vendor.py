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
from flask_restx import Resource
from flask import request, abort
import sqlalchemy

from bite_express import api, db
from bite_express.account.utils import (
    create_biteexer_account, assign_privilege, add_basic_info,
    secure_biteexer_acccount, create_biteexer_wallet
)
from bite_express.dbmodel import (
    BitexVendor, BiteExerLocation
)
from bite_express.utils import vendor_model


class Vendors(Resource):
    @api.doc("get_all_vendors")
    @api.marshal_list_with(vendor_model)  # serialize the result using vendor_model
    def get(self):
        """
        Get a list of all Vendors
        """
        vendors = (
            db.session.query(BitexVendor, BiteExerLocation)
                .join(
                    BiteExerLocation,
                    BitexVendor.bite_id==BiteExerLocation.bite_id,
                )
                .all()
        )

        # serialize each vendor's data into a dictionary and append it to the
        # result list
        result = []

        for vendor in vendors:
            # make this usable
            vendor_dict = {
                'id': vendor.BitexVendor.id,
                'bite_id': vendor.BitexVendor.bite_id,
                'kitchen_name': vendor.BitexVendor.kitchen_name,
                'website_url': vendor.BitexVendor.website_url,
                'logo': vendor.BitexVendor.logo,
                'bio': vendor.BitexVendor.bio,
                'opening_hour': vendor.BitexVendor.opening_hour,
                'closing_hour': vendor.BitexVendor.closing_hour,
                'rating': vendor.BitexVendor.rating,
                'date_created': vendor.BitexVendor.date_created,
                'date_updated': vendor.BitexVendor.date_updated,
                'location': {
                    'id': vendor.BiteExerLocation.id,
                    'country': vendor.BiteExerLocation.country,
                    'state_region': vendor.BiteExerLocation.state_region,
                    'city': vendor.BiteExerLocation.city,
                    'neighbourhood': vendor.BiteExerLocation.neighbourhood,
                    'post_code': vendor.BiteExerLocation.post_code,
                    'date_added': vendor.BiteExerLocation.date_added,
                    'date_updated': vendor.BiteExerLocation.date_updated,
                },
            }

            result.append(vendor_dict)

        return result


    @api.marshal_with(vendor_model)  # serialize the result using vendor_model
    @api.expect(vendor_model)
    def post(self):
        """
        Create a new Vendor
        """
        form_data = request.get_json()

        # create bite vendor account
        biteexer = create_biteexer_account(form_data)
        account_privilege = assign_privilege(biteexer, "Vendor")
        basic_info = add_basic_info(biteexer, form_data)
        account_security = secure_biteexer_acccount(biteexer, form_data)
        wallet = create_biteexer_wallet(biteexer)
        create_vendor = BitexVendor(bite_id=biteexer.bite_id)

        # add all biteexer data to db
        biteexer.add()
        account_privilege.add()
        basic_info.add()
        account_security.add()
        wallet.add()
        create_vendor.add()

        return biteexer, 201


class Vendor(Resource):
    @api.doc("get_a_vendor")
    @api.marshal_with(vendor_model)  # serialize the result using vendor_model
    def get(self, kitchen_name):
        """
        Get a Vendor by its Bite ID
        """
        try:
            vendor = (
                db.session.query(BitexVendor, BiteExerLocation)
                    .filter(BitexVendor.bite_id==kitchen_name)
                    .join(
                        BiteExerLocation,
                        BitexVendor.bite_id==BiteExerLocation.bite_id,
                    )
                    .one()
            )
            
            # serialize vendor data into a dictionary
            result = {
                'id': vendor.BitexVendor.id,
                'bite_id': vendor.BitexVendor.bite_id,
                'kitchen_name': vendor.BitexVendor.kitchen_name,
                'website_url': vendor.BitexVendor.website_url,
                'logo': vendor.BitexVendor.logo,
                'bio': vendor.BitexVendor.bio,
                'opening_hour': vendor.BitexVendor.opening_hour,
                'closing_hour': vendor.BitexVendor.closing_hour,
                'rating': vendor.BitexVendor.rating,
                'date_created': vendor.BitexVendor.date_created,
                'date_updated': vendor.BitexVendor.date_updated,
                'location': {
                    'id': vendor.BiteExerLocation.id,
                    'country': vendor.BiteExerLocation.country,
                    'state_region': vendor.BiteExerLocation.state_region,
                    'city': vendor.BiteExerLocation.city,
                    'neighbourhood': vendor.BiteExerLocation.neighbourhood,
                    'post_code': vendor.BiteExerLocation.post_code,
                    'date_added': vendor.BiteExerLocation.date_added,
                    'date_updated': vendor.BiteExerLocation.date_updated,
                },
            }
                
            return result
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)
            
            
    @api.marshal_with(vendor_model)  # serialize the result using vendor_model
    def put(self, kitchen_name):
        """
        Update a Vendor by its Bite ID
        """
        try:
            form_data = request.get_json()
            
            vendor = (
                db.session.query(BitexVendor, BiteExerLocation)
                    .filter(BitexVendor.bite_id==kitchen_name)
                    .join(
                        BiteExerLocation,
                        BitexVendor.bite_id==BiteExerLocation.bite_id,
                    )
                    .one()
            )
           
            vendor.BitexVendor.update(form_data.get("vendor")) 
            vendor.BiteExerLocation.update(form_data.get("vendor"))
            
            return vendor
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)


    @api.marshal_with(vendor_model)  # serialize the result using vendor_model
    def delete(self, kitchen_name):
        """
        Delete a Vendor by its Bite ID
        """
        try:
            vendor = (
                db.session.query(BitexVendor, BiteExerLocation)
                    .filter(BitexVendor.bite_id==kitchen_name)
                    .join(
                        BiteExerLocation,
                        BitexVendor.bite_id==BiteExerLocation.bite_id,
                    )
                    .one()
            )
           
            vendor.BitexVendor.delete()
            vendor.BiteExerLocation.delete()
            
            return vendor
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)
        

# register resource
api.add_resource(Vendors, "/v1/account/vendors")
api.add_resource(Vendor, "/v1/account/vendor/<string:kitchen_name>")
# api.add_resource(VendorMenus, "/v1/account/vendor/<string:kitchen_name>/menus")
