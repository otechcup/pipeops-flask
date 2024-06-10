#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bite Express App


__author__ = "PhoenixITng"
__copyright__ = "Copyright 2023 - datetime.utcnow().year, {}".format(__author__)
__credits__ = ["Mr. O"]
__version__ = "os.environ['BITE_EXPRESS_VERSION')"
__maintainer__ = __author__
__email__ = "support@bitexpress.ng"
__status__ = "os.environ['BITE_EXPRESS_ENVIRONMENT_STATUS')"


# import modules
from flask_restx import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_optional
)

from bite_express import bcrypt
from bite_express.dbmodel import BiteExer
from bite_express.permission.checker import is_authenticated
from bite_express.settings.current_biteexer import current_biteexer
from .forms import signin_model
from .routes import auth


@auth.route("/sign-in", methods=["POST"])
class SignIn(Resource):
    @auth.expect(signin_model, validate=True)
    @jwt_optional
    def post(self):
        """
        Authenticate and authorize a BiteExer account
        """
        biteexer = current_biteexer()
        _is_authenticated = is_authenticated(biteexer)
        
        if _is_authenticated:
            return make_response(
                jsonify(_is_authenticated), 400
            )
        
        form_data = request.get_json()
        
        biteexer = (
            BiteExer.get_by_email_address(
                form_data["email_address"].lower().strip()
            )
        )

        if (biteexer 
            and bcrypt.check_password_hash(
                biteexer._basic_info.account_security.password_hash,
                form_data["password"],
            )
        ):    
            access_token = create_access_token(
                identity=biteexer.bite_id,
            )
            refresh_token = create_refresh_token(
                identity=biteexer.bite_id,
            )
            
            return make_response(
                jsonify(
                    {
                        'message': {
                            'access_token': access_token,
                            'refresh_token': refresh_token,
                        },
                    },
                ), 201
            )
        else:
            return make_response(
                jsonify(
                    {
                        'message': (
                            "Email Address: {} or Password: {} - (is incorrect!). Kindly provide a valid sign in "
                            "credentials.".format(
                                form_data["email_address"].lower().strip(),
                                form_data["password"],
                            )
                        ),
                    },
                ), 401
            )
