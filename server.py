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

from bite_express import create_bite_express_app, db
from bite_express.dbmodel import *
from bite_express.config import *


# Set the appropriate config based on the environment settings
configs = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
}
env = config("BITE_EXPRESS_ENVIRONMENT_STATUS", cast=str).lower()
use_config = configs[env]    
bite_express_app = create_bite_express_app(use_config)


@bite_express_app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'BiteExer': BiteExer,
        'BiteExerAccountPrivilege': BiteExerAccountPrivilege,
        'BiteExerBasicInfo': BiteExerBasicInfo,
        'BiteExerLocation': BiteExerLocation,
        'BiteExerAccountSecurity': BiteExerAccountSecurity,
        'BitexVendor': BitexVendor,
        'BiteExerCreditCard': BiteExerCreditCard,
        'BiteExerWallet': BiteExerWallet,
        'BitexVendorMenu': BitexVendorMenu,
        'BiteExerOrderHistory': BiteExerOrderHistory,
        'BitexDriver': BitexDriver,
        'BitexDriverVehicle': BitexDriverVehicle,
        'BiteExpressExpenditure': BiteExpressExpenditure,
        'BiteExerTransactionHistory': BiteExerTransactionHistory,
    }


if __name__ == "__main__":
    bite_express_app.run(host='0.0.0.0', debug=False)
    
    # Use PORT environment variable if available, or default to 5000
    #port = int(os.environ.get('PORT', 5000))
    #app.run( port=port)
