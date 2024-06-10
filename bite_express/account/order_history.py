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
from flask_jwt_extended import jwt_required

from decimal import Decimal

from .routes import order_history
from .forms import order_history_model, order_history_form_model
from bite_express.settings.current_biteexer import current_biteexer
from bite_express.dbmodel import BiteExerOrderHistory, BitexVendorMenu
from bite_express.permission.checker import is_biteexer, is_bitex_title
from bite_express.expenditure import checkout_exp


@order_history.route("", methods=["POST", "GET"])
class OrderHistories(Resource):
    @order_history.marshal_list_with(order_history_model)
    @jwt_required()
    def get(self):
        """
        Get a list of all BitexUser/BitexAgent order history
        """
        biteexer = current_biteexer()
        not_biteexer = is_biteexer(biteexer)

        if not not_biteexer[0]:
            # improve this error handling message
            abort(404, not_biteexer[1]["message"])
            
        _is_bitex_title = is_bitex_title(
            biteexer, ["BitexUser", "BitexAgent", "BitexVendor"]
        )
        
        if _is_bitex_title[0]:
            bitex_ua_order_history = (
                BiteExerOrderHistory.query
                    .join(
                        BitexVendorMenu,
                        (
                            BiteExerOrderHistory.bitem_id
                            == BitexVendorMenu.bitem_id
                        ),
                    )
                    .filter(
                        (BiteExerOrderHistory.bite_id == biteexer.bite_id)
                        | (
                            BitexVendorMenu.kitchen_name
                            == biteexer.vendor.kitchen_name
                        )
                    )
                    .all()
            )
        else:
            bitex_ua_order_history = BiteExerOrderHistory.query.all()

        return bitex_ua_order_history


    @order_history.expect(order_history_form_model, validate=True)
    @jwt_required()
    def post(self):
        """
        Create a new order history
        """
        biteexer = current_biteexer()
        not_biteexer = is_biteexer(biteexer)
        _is_bitex_title = is_bitex_title(biteexer, ["BitexAgent", "BitexUser"])

        if not not_biteexer[0]:
            return make_response(jsonify(not_biteexer[1]), 404)

        # check if the biteexer has activate account

        if _is_bitex_title[0]:
            form_data = request.get_json()
            zero_balance =  Decimal("0.00")
            total_price = zero_balance
            
            for bitem in form_data["order_history"]:
                total_price += Decimal(bitem["price"]) * bitem["quantity"]
                
                validate_bitem_id = (
                    BitexVendorMenu.query
                        .filter_by(bitem_id=bitem["bitem_id"].strip())
                        .first()
                )
                
                if not validate_bitem_id:
                    return make_response(
                        jsonify(
                            {'message': "Sorry, bitem does not exist."},
                        ), 422
                    )
                   
                if Decimal(bitem["price"]) < validate_bitem_id.price:
                    return make_response(
                        jsonify(
                            {'message': "Sorry, the bitem price is more than that."},
                        ), 422
                    )
            
            if biteexer.wallet.wallet_balance - total_price < zero_balance:
                return make_response(
                    jsonify(
                        {'message': "Sorry, insufficient wallet balance."},
                    ), 422
                )
            
            for bitem in form_data["order_history"]:
                order_history = BiteExerOrderHistory(
                    bite_id=biteexer.bite_id,
                    bitem_id=bitem["bitem_id"].strip(),
                    price=Decimal(bitem["price"]),
                    quantity=bitem["quantity"],
                    destination=bitem["destination"].strip(),
                )

                order_history.add()

            checkout_exp(biteexer, total_price)
            
            return make_response(
                jsonify(
                    {'message': "Order history created successfully."},
                ), 201
            )
        else:
            return make_response(jsonify(_is_bitex_title[1]), 401)
