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
from flask_jwt_extended import get_jwt_identity

from bite_express.dbmodel import BiteExer


def current_biteexer() -> object:
    bite_id = get_jwt_identity()
    
    biteexer = BiteExer.get_by_bite_id(bite_id)
    
    return biteexer


class CurrentUser:
    def __init__(self):
        self.bite_id = get_jwt_identity()
        
        self.biteexer = BiteExer.get_by_bite_id(self.bite_id)
        
        self.is_authenticated()
        self.is_biteexer()
    
        
    def get_biteexer(self):
        return self.biteexer
    
    
    def is_authenticated(self):
        if self.biteexer:
            return {'message': "You are already signed in."}
        return None
    
    
    def is_biteexer(self):
        if self.biteexer is None:
            return {
                'message': "BiteExer does not exist! Please verify and try again.",
            }
        return None
    
    
    def has_setup_bitex_vendor_account(self):
        pass
    