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
import logging
from multiprocessing.connection import Client, Listener

_ERROR = 'error'
_RESULT = 'result'
_METHOD = 'method'
_ARGUMENT = 'argument'


class DeviceUnconnectedException(Exception):

    def __str__(self):
        return 'device not connected'


class DriverProcess(object):

    _address = None
    _device = None

    def __init__(self, address, device):
        self._address = address
        self._device = device

    def __del__(self):
        pass

    def run(self):

        print('binding socket...')
        listener = Listener(self._address, authkey=b'secret password')

        print('server running...')
        while True:
            try:
                self.handle_requests(self._device, listener)

            except KeyboardInterrupt:
                break

            except DeviceUnconnectedException:
                print('try to recover connection')
                # try to recover
                try:
                    self._device.start_communication()

                except Exception:
                    pass

                continue

            except Exception as e:
                print(str(e))
                # retry
                continue

        listener.close()

    def handle_requests(self, device, listener):

        while True:

            conn = None
            try:
                conn.close()

            except Exception:
                pass

            conn = listener.accept()

            response = {}

            try:
                request_string = conn.recv()
                request = json.loads(request_string)

            except ValueError as e:
                response[_ERROR] = str(e)
                conn.send_json(response)
                continue

            method = request[_METHOD]
            argument = request[_ARGUMENT]

            response = request.copy()

            if not _METHOD in request:
                response[_ERROR] = '"method" is missing'

            else:
                try:
                    response[_RESULT] = device.request(method, argument)

                except Exception as e:
                    response[_ERROR] = str(e)
                    conn.send(json.dumps(response))
                    raise e

            conn.send(json.dumps(response))


class RequestDriverProcess(object):
    """
    Accessing the background driver process (operating as client)

    Methods
    -------
    request(method)
        Request the driver process

    """

    _address = None

    def __init__(self, address):
        self._address = address

    def request(self, method, argument=None):
        """
        Requesting driver process

        Parameters
        ----------
        method : RequestData
            String for identifying an action to be requested

        Returns
        -------
        String
            Result of requested method

        Raises
        ------
        Exception
            If response of request contains the error field or connection failed

        """
        try:
            conn = Client(self._address, authkey='secret password')
            
            json_dict = {
                _METHOD: method,
                _ARGUMENT: argument,
            }
            conn.send(json.dumps(json_dict))

            response = json.loads(conn.recv())

            conn.close()

        except Exception as e:
            logging.error(str(e), exc_info=True)
            raise e

        if _ERROR in response:
            raise Exception(response[_ERROR])

        return response[_RESULT]
