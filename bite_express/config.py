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
from decouple import config

from datetime import timedelta


class Config:
    # secret key
    SECRET_KEY = config("BITE_EXPRESS_SECRET_KEY", cast=str)

    # jwt setting
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    PROPAGATE_EXCEPTIONS = True


class DevConfig(Config):
    DEBUG = True
    
    # db
    SQLALCHEMY_DATABASE_URI = "{dialect}:///{file_path}/{dbname}.db?{query}".format(
        dialect="sqlite",
        file_path="db",
        dbname="BiteExpressDB",
        query="charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    DEBUG = False
    
    # db
    SQLALCHEMY_DATABASE_URI = (
        "{dialect}+{driver}://{username}:{password}@{hostname}:{port}/{dbname}?{query}".format(
            dialect="mysql",
            driver="pymysql",
            username=config("BITE_EXPRESS_DATABASE_USERNAME", cast=str),
            password=config("BITE_EXPRESS_DATABASE_PASSWORD", cast=str),
            hostname="mysql1004.mochahost.com",
            port="3306",
            dbname="josiah87_BiteExpressDataStore",
            query="charset=utf8mb4",
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'connect_timeout': 60,
        },
        'pool_pre_ping': True,
        'pool_size' : 100,
        'pool_recycle': 3600, # 1 hour 300
    }


class TestConfig(Config):
    DEBUG = True
    TESTING = True
