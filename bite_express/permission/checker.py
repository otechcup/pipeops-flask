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


def has_setup_bitex_vendor_account(current_biteexer: object) -> dict:
    if current_biteexer.vendor.kitchen_name is None:
        return {
            'message': (
                "BitexVendor account setup error. Kindly update your (Personal Details, About BitexVendor and Location "
                "Information) BitexVendor account settings for absolute recognition."
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


def is_verified(current_biteexer: object) -> dict:
    pass


def has_activate_account(current_biteexer: object) -> bool:
    pass


def is_bitex_title(current_biteexer: object, title: list) -> tuple:
    if current_biteexer.privilege.title in title:
        return True,

    return False, {'message': f"Invalid credentials, unknown {title}."}
