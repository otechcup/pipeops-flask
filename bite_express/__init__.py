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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import pymysql


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt_manager = JWTManager()
cors = CORS()
api = Api(
    title="BiteExpress API",
    version="1.0",
    description="A food delivery app",
    doc="/",
)

pymysql.install_as_MySQLdb()


def create_bite_express_app(config):
    bite_express_app = Flask(__name__)

    bite_express_app.config.from_object(config)

    # initialize extensions
    db.init_app(bite_express_app)
    migrate.init_app(
        bite_express_app, db, render_as_batch=True, compare_type=True
    )
    api.init_app(bite_express_app)
    bcrypt.init_app(bite_express_app)
    jwt_manager.init_app(bite_express_app)
    cors.init_app(bite_express_app)


    # import namespaces
    from bite_express.auth.routes import auth
    from bite_express.account.routes import menu, biteexer, order_history


    # register namespaces
    api.add_namespace(auth)
    api.add_namespace(menu)
    api.add_namespace(biteexer)
    api.add_namespace(order_history)

    return bite_express_app
