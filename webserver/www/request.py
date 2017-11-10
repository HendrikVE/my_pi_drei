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

from Display import Display

LOGFILE = 'request.log'
LOGGING_FORMAT = '[%(levelname)s]: %(asctime)s\n'\
                 + 'in %(filename)s in %(funcName)s on line %(lineno)d\n'\
                 + '%(message)s\n'

SECRET_KEY = 'meinkey'

pi_results = {
    'displayState': None, # on or off
    'displayIntensity': None, # 0-1023
    'temperature': None, # int
    'humidity': None, # int
    'error': None,
}


def main():

    request_body = sys.stdin.read()
    pi_results['temperature'] = request_body
    is_valid = is_valid_signature(os.environ['HTTP_MESSAGE_SIGNATURE'], SECRET_KEY, request_body)

    if is_valid:

        print('EINS')

        # stdin already read out, so assign fp to FieldStorage
        tmpfile = tempfile.TemporaryFile()
        tmpfile.write(request_body)
        tmpfile.seek(0)
        form = cgi.FieldStorage(fp=tmpfile)
        tmpfile.close()

        print('ZWEI')

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
        print_error()


def is_valid_signature(signature, secret_key, body):

    computed_signature = 'sha512=' + hmac.new(secret_key, body, hashlib.sha512).hexdigest()

    return computed_signature == signature


def print_result(result):

    print ('Content-Type: text/html')
    print ('\n\r')
    print (result)


def print_error():

    print ('Status: 403 Forbidden')
    print ('\n\r')


if __name__ == '__main__':

    logging.basicConfig(filename=LOGFILE, format=LOGGING_FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        pi_results['error'] = str(e)

        print_result(json.dumps(pi_results))
