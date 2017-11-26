#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import zmq

from _ArduinoNano import ArduinoNano, RequestData, TempScale, DeviceUnconnectedException

PORT = 7000
ADDRESS = 'tcp://127.0.0.1:%i' % PORT


def main():

    global socket

    while True:

        response = {}

        try:
            request = socket.recv_json()

        except ValueError as e:
            response['error'] = str(e)
            socket.send_json(response)
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
                socket.send_json(response)
                raise e

        socket.send_json(response)


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
    socket = context.socket(zmq.REP)
    socket.bind(ADDRESS)

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