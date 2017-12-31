#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging
import zmq

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
        context = zmq.Context()
        server_socket = context.socket(zmq.REP)
        server_socket.bind(self._address)

        print('server running...')
        while True:
            try:
                self.handle_requests(self._device, server_socket)

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

    def handle_requests(self, device, server_socket):

        while True:

            response = {}

            try:
                request = server_socket.recv_json()

            except ValueError as e:
                response[_ERROR] = str(e)
                server_socket.send_json(response)
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
                    server_socket.send_json(response)
                    raise e

            server_socket.send_json(response)


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

    def request(self, method, argument):
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
            context = zmq.Context()
            client_socket = context.socket(zmq.REQ)
            client_socket.connect(self._address)

            json = {
                _METHOD: method,
                _ARGUMENT: argument,
            }
            client_socket.send_json(json)

            response = client_socket.recv_json()

            client_socket.disconnect(self._address)

        except Exception as e:
            logging.error(str(e), exc_info=True)
            raise e

        if _ERROR in response:
            raise Exception(response[_ERROR])

        return response[_RESULT]
