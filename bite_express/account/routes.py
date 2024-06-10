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


menu = Namespace(
    name="menu",  # backup (name="Menu",)
    description="BitexVendor menu namespace",
    path="/v1/menu",
)
biteexer = Namespace(
    name="biteexer",  # backup (name="Biteexer",)
    description="BiteExer namespace",
    path="/v1/biteexer",
)
order_history = Namespace(
    name="order history",
    description="BitexUser/BitexAgent order history namespace",
    path="/v1/order-history",
)


# circular import modules
from .biteexer import *
# from .vendor import *
from .menu import *
from .order_history import *
