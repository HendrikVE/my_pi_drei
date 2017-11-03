#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import Adafruit_DHT

class DHT22(object):

    _sensor = Adafruit_DHT.DHT22
    _gpio_pin = None

    def __init__(self, gpio_pin):
        _gpio_pin = gpio_pin

    def get_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(_sensor, pin)
        return temperature

    def get_humidity(self):
        humidity, temperature = Adafruit_DHT.read_retry(_sensor, pin)
        return humidity
