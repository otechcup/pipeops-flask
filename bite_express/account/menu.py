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
from flask_restx import Resource, abort
from flask import request, jsonify, make_response
import sqlalchemy
from flask_jwt_extended import jwt_required

import secrets
from datetime import datetime

from .routes import menu
from .forms import bitex_vendor_menu_model, menu_form_model
from bite_express.settings.current_biteexer import current_biteexer
from bite_express.dbmodel import BitexVendorMenu
from bite_express.permission.checker import (
    has_setup_bitex_vendor_account, is_biteexer, is_bitex_title
)


@menu.route("", methods=["POST", "GET"])
class Menus(Resource):
    @menu.marshal_list_with(bitex_vendor_menu_model)
    @jwt_required()
    def get(self):
        """
        Get a list of all BitexVendor menu and menu of a specific BitexVendor
        """
        biteexer = current_biteexer()
        not_biteexer = is_biteexer(biteexer)
        
        if not not_biteexer[0]:
            abort(404, not_biteexer[1]["message"])  # improve this error handling message
        
        _is_bitex_title = is_bitex_title(biteexer, ["BitexVendor"])
        
        if _is_bitex_title[0]:
            bitex_vendor_menus = (
                BitexVendorMenu.query
                    .filter_by(kitchen_name=biteexer.vendor.kitchen_name)
                    .all()
            )
        else:
            bitex_vendor_menus = BitexVendorMenu.query.all()

        return bitex_vendor_menus


    @menu.expect(menu_form_model, validate=True)
    @jwt_required()
    def post(self):
        """
        Create a new menu Bitem
        """
        biteexer = current_biteexer()
        not_biteexer = is_biteexer(biteexer)
        _is_bitex_title = is_bitex_title(biteexer, ["BitexVendor"])
        
        if not not_biteexer[0]:
            return make_response(jsonify(not_biteexer[1]), 404)
        
        # check if the biteexer has activate account
        
        if _is_bitex_title[0]:
            form_data = request.get_json()
            form_errors = []
            
            has_not_setup_vendor_account = has_setup_bitex_vendor_account(
                biteexer,
            )
    
            if has_not_setup_vendor_account:
                return make_response(
                    jsonify(has_not_setup_vendor_account), 403
                )
            else:
                # check if the BitexVendor is verified
                
                if form_errors:
                    return make_response(jsonify(form_errors), 422)
                
                bitem_id = secrets.token_hex(7)
                get_apt = form_data["average_prep_time"].replace(":", "")
                average_prep_time = datetime.strptime(get_apt, "%I%M%S").time()
                
                bitem = BitexVendorMenu(
                    kitchen_name=biteexer.vendor.kitchen_name,
                    bitem_id=bitem_id,
                    bitem=form_data["bitem"].title().strip(),
                    image=form_data["image"],
                    description=form_data["description"].strip(),
                    category=form_data["category"].title().strip(),
                    price=form_data["price"],
                    average_prep_time=average_prep_time,
                )

                bitem.add()

                return make_response(
                    jsonify({'message': "Menu Bitem created successfully."}), 201
                )
        else:
            return make_response(jsonify(_is_bitex_title[1]), 401)


@menu.route("/detail/<string:bitem_id>", methods=["PUT", "GET", "DELETE"])
class Menu(Resource):
    @menu.marshal_with(bitex_vendor_menu_model)
    @jwt_required()
    def get(self, bitem_id):
        """
        Get detail of a specific menu Bitem
        """
        try:
            bitex_vendor = BitexVendorMenu.query.filter_by(bitem_id=bitem_id).one()

            return bitex_vendor
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)


    @menu.marshal_with(bitex_vendor_menu_model)
    @menu.expect(menu_form_model, validate=True)
    @jwt_required()
    def put(self, bitem_id):
        """
        Update an existing menu Bitem
        """
        try:
            form_data = request.get_json()
            get_apt = form_data["average_prep_time"].replace(":", "")
            average_prep_time = datetime.strptime(get_apt, "%I%M%S").time()

            bitex_vendor = BitexVendorMenu.query.filter_by(bitem_id=bitem_id).one()

            bitex_vendor.update(
                status=form_data["status"],
                bitem=form_data["bitem"],
                image=form_data["image"],
                description=form_data["description"],
                category=form_data["category"],
                price=form_data["price"],
                average_prep_time=average_prep_time,
            )

            return bitex_vendor
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)


    @menu.marshal_with(bitex_vendor_menu_model)
    @jwt_required()
    def delete(self, bitem_id):
        """
        Delete a menu Bitem
        """
        try:
            bitex_vendor = BitexVendorMenu.query.filter_by(bitem_id=bitem_id).one()
           
            bitex_vendor.delete()
            
            return bitex_vendor
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)
