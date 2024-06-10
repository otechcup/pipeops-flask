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
from flask_restx import Namespace


menu = Namespace(
    name="Menu",
    description="BiteVendor menu namespace",
    path="/v1/menu",
)
biteexer = Namespace(
    name="Biteexer",
    description="BiteExer namespace",
    path="/v1/biteexer",
)


# circular import modules
from .biteexer import *
# from .vendor import *
from .menu import *
