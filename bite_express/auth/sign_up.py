#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BiteExpress App


__author__ = "PhoenixITng"
__copyright__ = f"Copyright 2023 - datetime.utcnow().year, {__author__}"
__credits__ = ["Mr. O"]
__version__ = "os.environ['BITE_EXPRESS_VERSION')"
__maintainer__ = __author__
__email__ = "info@biteexpress.ng"
__status__ = "os.environ['BITE_EXPRESS_ENVIRONMENT_STATUS')"


# import modules
from flask_restx import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required

import secrets

from .routes import auth
from .utils import hash_biteexer_password
from .forms import signup_model
from bite_express.settings.current_biteexer import current_biteexer
from bite_express.permission.checker import is_authenticated
from bite_express.dbmodel import (
    BiteExer, BiteExerAccountPrivilege, BiteExerBasicInfo, BiteExerWallet,
    BiteExerAccountSecurity, BitexVendor, BitexDriver
)


@auth.route("/sign-up", methods=["POST"])
class SignUp(Resource):
    @auth.expect(signup_model, validate=True)
    @jwt_required(optional=True)
    def post(self):
        """
        Create a BiteExer account for (BitexUser, BitexVendor, BitexDriver, BitexAgent) base on their account privilege title
        """
        biteexer = current_biteexer()
        _is_authenticated = is_authenticated(biteexer)
        
        if _is_authenticated:
            return make_response(
                jsonify(_is_authenticated), 400
            )
            
        form_data = request.get_json()
        form_errors = []
        
        validate_referrer_id = (
            BiteExer.query
                .filter_by(
                    bite_id=form_data["referrer_id"].upper().strip()
                )
                .first()
        )
        validate_email_address = (
            BiteExerBasicInfo.query
                .filter_by(
                    email_address=form_data["email_address"]
                        .lower()
                        .strip()
                )
                .first()
        )
        validate_phone_number = (
            BiteExerBasicInfo.query
                .filter_by(phone_number=form_data["phone_number"].strip())
                .first()
        )
        
        if validate_referrer_id is None:
            form_errors.append(
                {
                    'message': "Bite ID does not exist. Kindly verify if the Bite ID you enter is correct and existing.",
                    'field': "referrer_id",
                },
            )
            
        if validate_email_address:
            form_errors.append(
                {
                    'message': "Email address has been taken. Use a different one.",
                    'field': "email_address",
                },
            )
            
        if validate_phone_number:
            form_errors.append(
                {
                    'message': "Phone number has been taken. Use a different one.",
                    'field': "phone_number",
                }
            )
        
        if (form_data["title"].strip()
            not in ["BitexUser", "BitexVendor", "BitexDriver", "BitexAgent"]
        ):
            form_errors.append(
                {
                    'message': "BiteExer title does not exist. Use a different one.",
                    'field': "title",
                }
            )
        
        if len(form_data["password"]) < 8:
            form_errors.append(
                {
                    'message': "Password must be at least 8 characters long.",
                    'field': "password",
                }
            )
        
        if form_errors:
            return make_response(jsonify(form_errors), 422)
        
        if form_data["middle_name"] == None or " ":
            middle_name = None
        else:
            middle_name = form_data["middle_name"].title().strip()
        # backup this was commented out (
        # if form_data["middle_name"] == None or " ":
        #     middle_name = None
        # else:
        #     middle_name = form_data["middle_name"].title().strip()
        # )
        
        unique_id = secrets.token_hex(5)
        bite_id = unique_id[0:5] + "-BTE-" + unique_id[5:10]
        
        biteexer_account = BiteExer(
            referrer_id=form_data["referrer_id"].upper().strip(),
            bite_id=bite_id.upper(),
            first_name=form_data["first_name"].title().strip(),
            middle_name=middle_name,
            # backup (
            # middle_name=(
            #    None if form_data["middle_name"] == None or " "
            #    else form_data["middle_name"].title().strip()
            # ),
            # )
            last_name=form_data["last_name"].title().strip(),
        )
        account_privilege = BiteExerAccountPrivilege(
            bite_id=biteexer_account.bite_id,
            title=form_data["title"].strip(),
        )
        basic_info = BiteExerBasicInfo(
            bite_id=biteexer_account.bite_id,
            phone_number=form_data["phone_number"].strip(),
            email_address=form_data["email_address"].lower().strip(),
        )
        secure_account = BiteExerAccountSecurity(
            bite_id=biteexer_account.bite_id,
            password_hash=hash_biteexer_password(form_data),
        )
        wallet = BiteExerWallet(bite_id=biteexer_account.bite_id)
        
        biteexer_account.add()
        account_privilege.add()
        basic_info.add()
        secure_account.add()
        wallet.add()
        
        if account_privilege.title == "BitexVendor":
            bitex_vendor_account = BitexVendor(
                bite_id=biteexer_account.bite_id
            )
            
            bitex_vendor_account.add()
        elif account_privilege.title == "BitexDriver":
            bitex_driver_account = BitexDriver(
                bite_id=biteexer_account.bite_id
            )
        
            bitex_driver_account.add()
        
        return make_response(
            jsonify({'message': "BiteExer account created successfully."}), 201
        )
