#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time


class TempScale:
    CELSIUS, FAHRENHEIT = range(2)


class _RequestData:
    TEMP_CEL = "temp_cel",
    TEMP_FAH = "temp_fah",
    HEAT_INDEX_CEL = "heat_index_cel",
    HEAT_INDEX_FAH = "heat_index_fah",
    HUMIDITY = "humidity"


class ArduinoNano(object):

    class _SerialConnection(object):

        serial_connection = None

        def __init__(self, usb_path):
            self.serial_connection = serial.Serial(usb_path)
            time.sleep(5)  # wait for the arduino to reset after serial connection

        def __delete__(self, instance):
            self.serial_connection.close()

        def request(self, method_name):

            if not self.serial_connection.is_open:
                self.serial_connection.open()

            self.serial_connection.write(method_name)

            return self.serial_connection.readline()

    serialConnection = _SerialConnection('/dev/ttyUSB0')

    def get_temperature(self, scale):

        if scale == TempScale.CELSIUS:
            result = self.serialConnection.request('temp_cel')
            return float(result)

        elif scale == TempScale.FAHRENHEIT:
            result = self.serialConnection.request('temp_fah')
            return float(result)

        else:
            raise TypeError('not a valid TempScale')

    def get_heat_index(self, scale):

        if scale == TempScale.CELSIUS:
            result = self.serialConnection.request('heat_index_cel')
            return float(result)

        elif scale == TempScale.FAHRENHEIT:
            result = self.serialConnection.request('heat_index_fah')
            return float(result)

        else:
            raise TypeError('not a valid TempScale')

    def get_humidity(self):

        result = self.serialConnection.request('humidity')
        return float(result)