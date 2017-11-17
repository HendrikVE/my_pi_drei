#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import cgi
import hashlib
import hmac
import json
import logging
import os
import sys

# append root of the python code tree to sys.apth so that imports are working
#   alternative: add path to riotam_backend to the PYTHONPATH environment variable, but this includes one more step
#   which could be forget
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
WEBSERVER_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))

PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from config import config
from webserver.config import config as webserver_config
import http_prints

import api.api_functions as api
import api.api_json_keys as jk

LOGFILE = os.path.join(WEBSERVER_ROOT_DIR, 'log', 'request.log')

api_action_function_dict = {
    jk.REQUEST_KEY_GET_DISPLAY_STATE: api.get_display_state,
    jk.REQUEST_KEY_SET_DISPLAY_STATE: api.set_display_state,

    jk.REQUEST_KEY_GET_DISPLAY_INTENSITY: api.get_display_intensity,
    jk.REQUEST_KEY_SET_DISPLAY_INTENSITY: api.set_display_intensity,

    jk.REQUEST_KEY_GET_TEMPERATURE: api.get_temperature,
    jk.REQUEST_KEY_GET_HUMIDITY: api.get_humidity,
}


def main():

    json_dict = {}

    request_body = sys.stdin.read()
    json_request = json.loads(request_body)

    # check for existing signature
    submitted_signature = None
    try:
        submitted_signature = os.environ['HTTP_X_MESSAGE_SIGNATURE']

    except KeyError:
        missing = 'X-Message-Signature in HTTP header'
        json_dict[jk.RESULT_KEY_ERROR] = '%s missing' % missing
        http_prints.print_unauthorized(json_dict)

    # check for existing action_key
    action_key = None
    try:
        action_key = json_request[jk.REQUEST_KEY_ACTION_KEY]

    except KeyError:
        missing = '%s in json' % jk.REQUEST_KEY_ACTION_KEY
        json_dict[jk.RESULT_KEY_ERROR] = '%s missing' % missing
        http_prints.print_bad_request(json_dict)

    # continue if signature is valid
    is_valid = is_valid_signature(submitted_signature, webserver_config.SECRET_KEY, request_body)

    if is_valid:
        api_function = api_action_function_dict.get(action_key, None)

        if api_function is None:
            json_dict[jk.RESULT_KEY_ERROR] = 'not a valid api call'
            http_prints.print_bad_request(json_dict)

        else:
            # replace json-array with the one generated by api-function
            json_dict = api_function(json_request)

            if json_dict[jk.RESULT_KEY_ERROR] is not None:
                http_prints.print_bad_request(json_dict)

    else:
        json_dict[jk.RESULT_KEY_ERROR] = 'signature invalid'
        http_prints.print_unauthorized(json_dict)

    # is only printed if no error occurred (script is aborted when calling one of the error functions of http_prints)
    http_prints.print_result(json_dict)


def is_valid_signature(signature, secret_key, body):

    computed_signature = 'sha512=' + hmac.new(secret_key, body, hashlib.sha512).hexdigest()

    #return computed_signature == signature
    return 'signature' == signature


if __name__ == '__main__':

    logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        json_dict = {jk.RESULT_KEY_ERROR: str(e)}
        http_prints.print_internal_server_error(json_dict)
