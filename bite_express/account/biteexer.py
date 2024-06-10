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
from flask_jwt_extended import jwt_required

from .routes import biteexer
from .forms import biteexer_model
from bite_express.dbmodel import BiteExer
from bite_express.settings.current_biteexer import current_biteexer


@biteexer.route("", methods=["GET"])  # backup (@biteexer.route("/", methods=["GET", "PUT"]))
class BiteExer_(Resource):
    @biteexer.marshal_list_with(biteexer_model)  # backup (@biteexer.marshal_with(biteexer_model))
    @jwt_required()
    def get(self):
        """
        Get all profile information of a BiteExer
        """
        try:
            biteexer = current_biteexer()
            
            profile_info = (
                BiteExer.query.filter_by(bite_id=biteexer.bite_id).one()
            )
            
            return profile_info
        except Exception:
            abort(404)


@biteexer.route("/wallet/balance/top-up", methods=["POST"])
class WalletBalanceTopUp(Resource):
    @biteexer.marshal_list_with(biteexer_model)
    @jwt_required()
    def post(self):
        """
        Top-up BiteExer wallet balance
        """
        pass
