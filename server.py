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
from bite_express import create_bite_express_app, db
from bite_express.dbmodel import *


bite_express_app = create_bite_express_app()


@bite_express_app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'BiteExer': BiteExer,
        'BiteExerAccountPrivilege': BiteExerAccountPrivilege,
        'BiteExerBasicInfo': BiteExerBasicInfo,
        'BiteExerLocation': BiteExerLocation,
        'BiteExerAccountSecurity': BiteExerAccountSecurity,
        'BiteVendor': BiteVendor,
        'BiteExerCreditCard': BiteExerCreditCard,
        'BiteExerWallet': BiteExerWallet,
        'BiteVendorMenu': BiteVendorMenu,
        'BiteExerOrderHistory': BiteExerOrderHistory,
        'BiteDriver': BiteDriver,
        'BiteDriverVehicle': BiteDriverVehicle,
        'BiteExpressExpenditure': BiteExpressExpenditure,
        'BiteExerTransactionHistory': BiteExerTransactionHistory,
    }


if __name__ == "__main__":
    bite_express_app.run(debug=True)
