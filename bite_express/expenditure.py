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
from decimal import Decimal

from bite_express.dbmodel import BiteExpressExpenditure


def checkout_exp(current_biteexer: object, credit: Decimal):    
    get_checkout_vat_expenditure = (
        BiteExpressExpenditure.query
            .filter_by(category="Checkout VAT")
            .first()
    )
    get_biteexer_funds_expenditure = (
        BiteExpressExpenditure.query
            .filter_by(category="BiteExer Funds")
            .first()
    )
    get_checkout_funds_expenditure = (
        BiteExpressExpenditure.query
            .filter_by(category="Checkout Funds")
            .first()
    )
    
    checkout_vat_share = credit * get_checkout_vat_expenditure.share
    carcvs = credit - checkout_vat_share  # credit after removing checkout vat share
    
    current_biteexer.wallet.debit_wallet_balance(credit)
    get_biteexer_funds_expenditure.update_debit(credit)
    get_checkout_vat_expenditure.update_creadit(checkout_vat_share)
    get_checkout_funds_expenditure.update_creadit(carcvs)
    