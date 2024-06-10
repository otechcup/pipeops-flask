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


def has_setup_vendor_account(current_biteexer: object) -> dict:
    if current_biteexer.vendor.kitchen_name is None:
        return {
            'message': (
                "Bite Vendor account setup error. Kindly update your (Personal Details, About Vendor and Location Information) "
                "Bite Vendor account settings for absolute recognition."
            ),
        }


def is_biteexer(current_biteexer: object) -> tuple:
    if current_biteexer is None:
        return (
            False, 
            {
                'message': "BiteExer does not exist! Please verify and try again.",
            },
        )

    return True,


def is_authenticated(current_biteexer: object) -> dict:
    if current_biteexer:
        return {'message': "You are already signed in."}


def is_vendor(current_biteexer: object) -> tuple:
    if current_biteexer.privilege.title == "Vendor":
        return True,

    return False, {'message': "Invalid credentials, unknown Bite Vendor."}
    
    
def is_restricted_on_pt(current_biteexer: object, restricted_pt: list) -> dict:  # on privilege title
    if current_biteexer.privilege.title in restricted_pt:
        return {
            'message': "Invalid credentials, you don't have access to this system."
        }


def is_verified(current_biteexer: object) -> dict:
    pass


def has_activate_account(current_biteexer: object) -> bool:
    pass
