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
from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required
import sqlalchemy

from .routes import biteexer
from .forms import biteexer_model
from bite_express.dbmodel import BiteExer
from bite_express.settings.current_biteexer import current_biteexer


@biteexer.route("/", methods=["GET", "PUT"])
class BiteEr(Resource):
    @biteexer.marshal_with(biteexer_model)
    @jwt_required
    def get(self):
        """
        Get all profile information of a specific BiteExer
        """
        try:
            biteexer = current_biteexer()
            
            profile_info = (
                BiteExer.query.filter_by(bite_id=biteexer.bite_id).one()
            )
            
            return profile_info
        except sqlalchemy.orm.exc.NoResultFound:
            abort(404)
    
    
    # def put(self):
    #     """
    #     Update BiteExer profile information
    #     """
    #     pass
