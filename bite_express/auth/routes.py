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
from flask_restx import Namespace


auth = Namespace(
    name="auth",  # backup (name="Auth",)
    description="BiteExer authentication namespace",
    path="/v1/auth",
)


# circular import modules
from .sign_in import *
from .sign_up import *
from .refresh import *
