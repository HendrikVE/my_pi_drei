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
import tempfile

# append root of the python code tree to sys.apth so that imports are working
#   alternative: add path to riotam_backend to the PYTHONPATH environment variable, but this includes one more step
#   which could be forget
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from drivers.adafruit_22_display.Display import Display
from webserver.config import config

LOGFILE = 'request.log'

pi_results = {
    'displayState': None,  # on or off
    'displayIntensity': None,  # 0-1023
    'temperature': None,  # int
    'humidity': None,  # int
    'error': None,
}


def main():

    request_body = sys.stdin.read()

    submitted_signature = None
    try:
        submitted_signature = os.environ['HTTP_X_MESSAGE_SIGNATURE']
    except KeyError:
        print_error('X-Message-Signature header missing')

    is_valid = is_valid_signature(submitted_signature, config.SECRET_KEY, request_body)

    if is_valid:

        form = get_field_storage(request_body)

        action = form.getfirst('action')

        display = Display()
        if action == '1':
            display.turn_on()
            pi_results['displayState'] = 'on'
        elif action == '2':
            display.turn_off()
            pi_results['displayState'] = 'off'

        print_result(json.dumps(pi_results))

    else:
        print_error('signature invalid')


def get_field_storage(request_body):

    # stdin already read out, so assign fp to FieldStorage
    tmpfile = tempfile.TemporaryFile()
    tmpfile.write(request_body)
    tmpfile.seek(0)
    form = cgi.FieldStorage(fp=tmpfile)
    tmpfile.close()

    return form


def is_valid_signature(signature, secret_key, body):

    computed_signature = 'sha512=' + hmac.new(secret_key, body, hashlib.sha512).hexdigest()

    #return computed_signature == signature
    return "signature" == signature


def print_result(result):

    print('Content-Type: text/html')
    print('\n\r')
    print(result)


def print_error(error_message):

    print('Status: 403 Forbidden')
    print('\n\r')
    print(error_message)
    sys.exit()


if __name__ == '__main__':

    logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        pi_results['error'] = str(e)

        print_result(json.dumps(pi_results))
