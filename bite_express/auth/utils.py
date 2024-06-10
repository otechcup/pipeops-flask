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
from bite_express import bcrypt


def hash_biteexer_password(form_data: dict) -> str:
    hash_password = bcrypt.generate_password_hash(
        form_data["password"]
    ).decode("utf-8")

    return hash_password
