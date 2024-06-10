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
from os import urandom

from bite_express.auth.utils import hash_biteexer_password
from bite_express.dbmodel import (
    BiteExer, BiteExerAccountPrivilege, BiteExerBasicInfo, BiteExerAccountSecurity,
    BiteExerWallet,
)


def generate_bite_id() -> str:
    unique_id = urandom(5).hex()
    bite_id = unique_id[0:5] + "-BTE-" + unique_id[5:10]
    
    return bite_id.upper()
        

def create_biteexer_account(form_data: dict) -> object:
    if form_data.get("middle_name") == None:
        middle_name = None
    else:
        middle_name = form_data.get("middle_name").title().strip()
    
    biteexer_account = BiteExer(
        referral_id=form_data.get("referral_id").upper().strip(),
        bite_id=generate_bite_id(),
        first_name=form_data.get("first_name").title().strip(),
        middle_name=middle_name,
        last_name=form_data.get("last_name").title().strip(),
    )
    
    return biteexer_account


def assign_privilege(biteexer: object, title: str) -> object:
    account_privilege = BiteExerAccountPrivilege(
        bite_id=biteexer.bite_id,
        title=title,
    )
    
    return account_privilege


def add_basic_info(biteexer: object, form_data: dict) -> object:
    basic_info = BiteExerBasicInfo(
        bite_id=biteexer.bite_id,
        phone_number=form_data.get("phone_number").strip(),
        email_address=form_data.get("email_address").lower().strip(),
    )
    
    return basic_info


def secure_biteexer_acccount(biteexer: object, form_data: dict) -> object:
    secure_account = BiteExerAccountSecurity(
        bite_id=biteexer.bite_id,
        password_hash=hash_biteexer_password(form_data),
    )
    
    return secure_account


def create_biteexer_wallet(biteexer: object) -> object:
    wallet = BiteExerWallet(
        bite_id=biteexer.bite_id,
    )
    
    return wallet


def convert_timeobject(time: datetime):
    ...
