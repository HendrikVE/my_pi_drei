#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import json
import sys


def print_result(json_dict):
    __print_with_http_status__(200, json_dict)


def print_bad_request(json_dict):
    __print_with_http_status__(400, json_dict)
    sys.exit()


def print_unauthorized(json_dict):
    __print_with_http_status__(401, json_dict)
    sys.exit()


def print_internal_server_error(json_dict):
    __print_with_http_status__(500, json_dict)
    sys.exit()


def __print_with_http_status__(status_code, json_dict, output_string=None):

    if output_string is None:
        try:
            output_string = json.dumps(json_dict)

        except Exception as e:
            __print_with_http_status__(500, None, output_string=str(e))
            sys.exit()

    print('Content-Type: application/json')

    if status_code == 200:
        print('Status: 200 OK')

    elif status_code == 400:
        print('Status: 400 Bad Request')

    elif status_code == 401:
        print('Status: 401 Unauthorized')

    elif status_code == 500:
        print('Status: 500 Internal Server Error')

    print('\n\r')
    print(output_string)
