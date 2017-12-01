#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging

import time
import zmq

import _ArduinoNano
from _ArduinoNano import ArduinoNano, TempScale, DeviceUnconnectedException

PORT = 7000
ADDRESS = 'tcp://127.0.0.1:%i' % PORT

_ERROR = 'error'
_RESULT = 'result'
_METHOD = 'method'


# copy the RequestData class for accessing from Arduino
class RequestData(_ArduinoNano.RequestData):
    pass


class RequestDriverProcess(object):

    def request(self, method):
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
            return None

        if _ERROR in response:
            raise Exception(response[_ERROR])

        return response[_RESULT]


def main():

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

    return None


if __name__ == '__main__':

    print('starting arduino driver...')
    arduino_nano = ArduinoNano()

    while True:
        try:
            arduino_nano.start_communication()
            # established connection, break out of loop
            break

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