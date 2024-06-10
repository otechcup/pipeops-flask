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
from flask_restx import fields

from .routes import auth
from bite_express.utils import NullableString


signin_model = auth.model(
    "BiteExer Sign In",
    {
        'email_address': fields.String(
            required=True, min_length=2, max_length=500
        ),
        'password': fields.String(required=True, min_length=8),
    },
)
signup_model = auth.inherit(
    "BiteExer Sign Up",
    signin_model,
    {
        'first_name': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'middle_name': NullableString(max_length=100),
        'last_name': fields.String(
            required=True, min_length=2, max_length=100
        ),
        'referral_id': fields.String(required=True, max_length=15),
        'title': fields.String(required=True, min_length=2, max_length=300),
        'phone_number': fields.String(
            required=True, min_length=2, max_length=20
        ),
    },
)
