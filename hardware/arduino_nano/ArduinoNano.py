#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class TempScale:
    CELSIUS, FAHRENHEIT = range(2)


class ArduinoNano(object):

    def get_temperature(self, scale):

        if scale == TempScale.CELSIUS:
            return 21.0

        elif scale == TempScale.FAHRENHEIT:
            return  42.0

        else:
            raise TypeError('not a valid TempScale')

    def get_heat_index(self, scale):

        if scale == TempScale.CELSIUS:
            return 21.0

        elif scale == TempScale.FAHRENHEIT:
            return 42.0

        else:
            raise TypeError('not a valid TempScale')

    def get_humidity(self):

        return 71
