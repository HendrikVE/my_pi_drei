#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging

import zmq

import _ArduinoNano
from _ArduinoNano import ArduinoNano, TempScale, DeviceUnconnectedException

PORT = 7000
ADDRESS = 'tcp://127.0.0.1:%i' % PORT


# copy the RequestData class for accessing from Arduino
class RequestData(_ArduinoNano.RequestData):
    pass


class RequestDriverProcess(object):

    def request(self, method):
        try:
            context = zmq.Context()
            client_socket = context.socket(zmq.REQ)
            client_socket.connect(ADDRESS)

            json = {'method': method}
            client_socket.send_json(json)

            response = client_socket.recv_json()

            client_socket.disconnect(ADDRESS)

            return response['result']

        except Exception as e:
            logging.error(str(e), exc_info=True)
            return None


def main():

    global server_socket

    while True:

        response = {}

        try:
            request = server_socket.recv_json()

        except ValueError as e:
            response['error'] = str(e)
            server_socket.send_json(response)
            continue

        method = request['method']

        response = request.copy()

        if not 'method' in request:
            response['error'] = '"method" is missing'

        else:
            try:
                response = request_arduino(arduino_nano, response, method)

            except DeviceUnconnectedException as e:
                response['error'] = 'cant access data: device not connected'
                server_socket.send_json(response)
                raise e

        server_socket.send_json(response)


def request_arduino(arduino_nano, response, method):

    if method == RequestData.TEMP_CEL:
        response['result'] = arduino_nano.get_temperature(TempScale.CELSIUS)

    elif method == RequestData.TEMP_FAH:
        response['result'] = arduino_nano.get_temperature(TempScale.FAHRENHEIT)

    elif method == RequestData.HEAT_INDEX_CEL:
        response['result'] = arduino_nano.get_heat_index(TempScale.CELSIUS)

    elif method == RequestData.HEAT_INDEX_FAH:
        response['result'] = arduino_nano.get_heat_index(TempScale.FAHRENHEIT)

    elif method == RequestData.HUMIDITY:
        response['result'] = arduino_nano.get_humidity()

    return response


if __name__ == '__main__':

    print('starting arduino driver...')
    arduino_nano = ArduinoNano()
    arduino_nano.start_communication()

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
            print('try to recover conection')
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