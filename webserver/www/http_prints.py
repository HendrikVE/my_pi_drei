#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import json
import sys


def print_result(result_json):
    __print_with_http_status__(200, result_json)


def print_bad_request(result_json):
    __print_with_http_status__(400, result_json)
    sys.exit()


def print_unauthorized(result_json):
    __print_with_http_status__(401, result_json)
    sys.exit()


def print_internal_server_error(result_json):
    __print_with_http_status__(500, result_json)
    sys.exit()


def __print_with_http_status__(status_code, result_json, skip_json_dump=False):

    if not skip_json_dump:
        try:
            result_json = json.dumps(result_json)

        except TypeError as e:
            __print_with_http_status__(500, str(e), skip_json_dump=True)
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
    print(result_json)
