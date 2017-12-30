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
import time
import os
import sys
import zmq

# append root of the python code tree to sys.apth so that imports are working
CUR_DIR = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from hardware.arduino_nano._arduino_nano import ArduinoNano, DeviceUnconnectedException
from arduino.dht22.dht22_interface import TempScale, RequestData

PORT = 7000
ADDRESS = 'tcp://127.0.0.1:%i' % PORT

_ERROR = 'error'
_RESULT = 'result'
_METHOD = 'method'


class RequestDriverProcess(object):
    """
    Accessing the background driver process (operating as client)

    Methods
    -------
    request(method)
        Request the driver process

    """

    def request(self, method):
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
            client_socket.connect(ADDRESS)

            json = {_METHOD: method}
            client_socket.send_json(json)

            response = client_socket.recv_json()

            client_socket.disconnect(ADDRESS)

        except Exception as e:
            logging.error(str(e), exc_info=True)
            raise e

        if _ERROR in response:
            raise Exception(response[_ERROR])

        return response[_RESULT]


def main():
    """
    Run the Driver Process (operating as server)

    """

    global server_socket

    while True:

        response = {}

        try:
            request = server_socket.recv_json()

        except ValueError as e:
            response[_ERROR] = str(e)
            server_socket.send_json(response)
            continue

        method = request[_METHOD]

        response = request.copy()

        if not _METHOD in request:
            response[_ERROR] = '"method" is missing'

        else:
            try:
                response[_RESULT] = request_arduino(arduino_nano, method)

            except Exception as e:
                response[_ERROR] = str(e)
                server_socket.send_json(response)
                raise e

        server_socket.send_json(response)


def request_arduino(arduino_nano, method):
    """
    Requesting driver process

    Parameters
    ----------
    arduino_nano : ArduinoNano
        Device to request

    method : RequestData
        String for identifying an action to be requested

    Returns
    -------
    float or String
        Result of requested method

    Raises
    ------
    Exception
        Raised if invalid method is requested

    """

    if method == RequestData.TEMP_CEL:
        return arduino_nano.get_temperature(TempScale.CELSIUS)

    elif method == RequestData.TEMP_FAH:
        return arduino_nano.get_temperature(TempScale.FAHRENHEIT)

    elif method == RequestData.HEAT_INDEX_CEL:
        return arduino_nano.get_heat_index(TempScale.CELSIUS)

    elif method == RequestData.HEAT_INDEX_FAH:
        return arduino_nano.get_heat_index(TempScale.FAHRENHEIT)

    elif method == RequestData.HUMIDITY:
        return arduino_nano.get_humidity()

    raise Exception('invalid method: %s' % method)


if __name__ == '__main__':

    print('starting arduino driver...')
    arduino_nano = ArduinoNano()

    while True:
        try:
            arduino_nano.start_communication()
            # established connection, break out of loop
            break

        except KeyboardInterrupt:
            sys.exit()

        except Exception:
            # retry connection in 1 second
            time.sleep(1)
            continue

    print('binding socket...')
    context = zmq.Context()
    server_socket = context.socket(zmq.REP)
    server_socket.bind(ADDRESS)

    print('server running...')
    while True:
        try:
            main()

        except KeyboardInterrupt:
            break

        except DeviceUnconnectedException:
            print('try to recover connection')
            # try to recover
            try:
                arduino_nano.start_communication()

            except Exception:
                pass

            continue

        except Exception as e:
            print(str(e))
            # retry
            continue