#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

from serial import Serial, SerialException
import time
import os
import sys

# append root of the python code tree to sys.apth so that imports are working
CUR_DIR = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from arduino.dht22.dht22_interface import TempScale, RequestData


class DeviceUnconnectedException(Exception):

    def __str__(self):
        return 'device not connected'

    pass


class ArduinoNano(object):
    """
    Abstraction for a connected Arduino Nano

    Methods
    -------
    start_communication()
        Initiate the communication with the Arduino Nano

    stop_communication()
        Stop the communication with the Arduino Nano

    get_temperature(scale=TempScale.CELSIUS)
        Read out temperature from Arduino Nano

    get_heat_index(scale=TempScale.CELSIUS)
        Read out heat index from Arduino Nano

    get_humidity()
        Read out humidity from Arduino Nano

    """
    _serialConnection = None

    def start_communication(self):
        """
        Establish the serial connection to the device

        Raises
        ------
        SerialException
            Raised if something went wrong opening a serial connection to the device

        """
        try:
            self._serialConnection = _SerialConnection('/dev/ttyUSB0')
            self._serialConnection.open()

        except SerialException as e:
            raise e

    def stop_communication(self):
        """
        Close the serial connection to the device
        """
        self._serialConnection.close()

    def get_temperature(self, scale=TempScale.CELSIUS):
        """
        Read temperature from device

        Parameters
        ----------
        scale : TempScale, optional
            Used scale type for temperature. Default: TempScale.CELSIUS

        Returns
        -------
        float
            Temperature

        Raises
        ------
        TypeError
            In case of invalid scale type

        DeviceUnconnectedException
            Value could not be read, because device is not connected

        """
        if scale == TempScale.CELSIUS:
            result = self._serialConnection.request(RequestData.TEMP_CEL)
            return float(result)

        elif scale == TempScale.FAHRENHEIT:
            result = self._serialConnection.request(RequestData.TEMP_FAH)
            return float(result)

        else:
            raise TypeError('not a valid TempScale')

    def get_heat_index(self, scale=TempScale.CELSIUS):
        """
        Read heat index from device

        Parameters
        ----------
        scale : TempScale, optional
            Used scale type for temperature. Default: TempScale.CELSIUS

        Returns
        -------
        float
            Heat index

        Raises
        ------
        TypeError
            In case of invalid scale type

        DeviceUnconnectedException
            Value could not be read, because device is not connected

        """
        if scale == TempScale.CELSIUS:
            result = self._serialConnection.request(RequestData.HEAT_INDEX_CEL)
            return float(result)

        elif scale == TempScale.FAHRENHEIT:
            result = self._serialConnection.request(RequestData.HEAT_INDEX_FAH)
            return float(result)

        else:
            raise TypeError('not a valid TempScale')

    def get_humidity(self):
        """
        Read humidity from device

        Returns
        -------
        float
            Humidity (percentage)

        Raises
        ------
        DeviceUnconnectedException
            Value could not be read, because device is not connected

        """
        result = self._serialConnection.request(RequestData.HUMIDITY)
        return float(result)


class _SerialConnection(object):
    """
    Handling serial connection on USB

    """
    usb_path = ''
    serial_connection = None

    def __init__(self, usb_path):
        self.usb_path = usb_path

    def __delete__(self, instance):
        self.close()

    def open(self):
        self.serial_connection = Serial(self.usb_path)
        time.sleep(5)  # wait for the arduino to reset after serial connection

    def close(self):
        self.serial_connection.close()

    def request(self, method_name):

        try:

            if not self.serial_connection.is_open:
                self.serial_connection.open()

            self.serial_connection.write(method_name.encode('utf-8'))

            return self.serial_connection.readline()

        except Exception:
            raise DeviceUnconnectedException()


class _Cache(object):

    class CacheEntry(object):

        _key = None
        _value = None
        _creation_time = None
        _validity_period = None

        def __init__(self, key, value, validity_period=10):
            """
            Caching sensor data

            Parameters
            ----------
            key : String
                Key for the entry

            value : String
                Value of the entry

            validity_period : int, optional
                Amount of seconds, after which the entry is invalidated

            """
            self._key = key
            self._value = value
            self._creation_time = time.time()
            self._validity_period = validity_period

    _entries = []

    def add_entry(self, entry):
        self._entries.append(entry)

    def remove_entry(self, key):
        self._entries.remove(key)