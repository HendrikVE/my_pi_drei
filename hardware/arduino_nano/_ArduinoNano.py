#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import serial
import time


class TempScale:
    CELSIUS, FAHRENHEIT = range(2)


class RequestData:
    TEMP_CEL = 'temp_cel'
    TEMP_FAH = 'temp_fah'
    HEAT_INDEX_CEL = 'heat_index_cel'
    HEAT_INDEX_FAH = 'heat_index_fah'
    HUMIDITY = 'humidity'


class DeviceUnconnectedException(Exception):
    pass


class ArduinoNano(object):

    class _SerialConnection(object):

        usb_path = ''
        serial_connection = None

        def __init__(self, usb_path):
            self.usb_path = usb_path

        def __delete__(self, instance):
            self.close()

        def open(self):
            self.serial_connection = serial.Serial(self.usb_path)
            time.sleep(5)  # wait for the arduino to reset after serial connection

        def close(self):
            self.serial_connection.close()

        def request(self, method_name):

            try:

                if not self.serial_connection.is_open:
                    self.serial_connection.open()

                self.serial_connection.write(method_name)

                return self.serial_connection.readline()

            except Exception:
                raise DeviceUnconnectedException()

    serialConnection = None

    def start_communication(self):
        try:
            self.serialConnection = self._SerialConnection('/dev/ttyUSB0')
            self.serialConnection.open()

        except Exception as e:
            raise e

    def stop_communication(self):
        self.serialConnection.close()

    def get_temperature(self, scale):

        if scale == TempScale.CELSIUS:
            result = self.serialConnection.request(RequestData.TEMP_CEL)
            return float(result)

        elif scale == TempScale.FAHRENHEIT:
            result = self.serialConnection.request(RequestData.TEMP_FAH)
            return float(result)

        else:
            raise TypeError('not a valid TempScale')

    def get_heat_index(self, scale):

        if scale == TempScale.CELSIUS:
            result = self.serialConnection.request(RequestData.HEAT_INDEX_CEL)
            return float(result)

        elif scale == TempScale.FAHRENHEIT:
            result = self.serialConnection.request(RequestData.HEAT_INDEX_FAH)
            return float(result)

        else:
            raise TypeError('not a valid TempScale')

    def get_humidity(self):

        result = self.serialConnection.request(RequestData.HUMIDITY)
        return float(result)
