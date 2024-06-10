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
from flask_jwt_extended import jwt_required, create_access_token
from flask import jsonify, make_response

from .routes import auth
from bite_express.permission.checker import is_biteexer
from bite_express.settings.current_biteexer import current_biteexer


@auth.route("/refresh", methods=["POST"])
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh BiteExer account authentication and authorization
        """
        biteexer = current_biteexer()
        not_biteexer = is_biteexer(biteexer)
        
        if not not_biteexer[0]:
            return make_response(jsonify(not_biteexer[1]), 404)
            
        new_access_token = create_access_token(biteexer.bite_id)
            
        return make_response(
            jsonify({'message': {'access_token': new_access_token}}), 201
        )
