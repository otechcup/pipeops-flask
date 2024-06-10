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
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from bite_express.config import Config


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


def create_bite_express_app(config_class=Config):
    bite_express_app = Flask(__name__)

    bite_express_app.config.from_object(config_class)

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
    from bite_express.account.routes import menu
    from bite_express.account.routes import biteexer


    # register namespaces
    api.add_namespace(auth)
    api.add_namespace(menu)
    api.add_namespace(biteexer)

    return bite_express_app
