#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial


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

        class RequestMethod:
            TEMP_CEL = 'temp_cel',
            TEMP_FAH = 'temp_fah',
            HEAT_INDEX_CEL = 'heat_index_cel',
            HEAT_INDEX_FAH = 'heat_index_fah',
            HUMIDITY = 'humidity'

        serial_connection = None

        def __init__(self, usb_path):
            self.serial_connection = serial.Serial(usb_path)

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
            result = self.serialConnection.request(self._SerialConnection.RequestMethod.TEMP_CEL)
            return float(result)

        elif scale == TempScale.FAHRENHEIT:
            result = self.serialConnection.request(self._SerialConnection.RequestMethod.TEMP_FAH)
            return float(result)

        else:
            raise TypeError('not a valid TempScale')

    def get_heat_index(self, scale):

        if scale == TempScale.CELSIUS:
            result = self.serialConnection.request(self._SerialConnection.RequestMethod.HEAT_INDEX_CEL)
            return float(result)

        elif scale == TempScale.FAHRENHEIT:
            result = self.serialConnection.request(self._SerialConnection.RequestMethod.HEAT_INDEX_FAH)
            return float(result)

        else:
            raise TypeError('not a valid TempScale')

    def get_humidity(self):

        result = self.serialConnection.request(self._SerialConnection.RequestMethod.HUMIDITY)
        return float(result)
