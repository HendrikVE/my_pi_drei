#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

# append root of the python code tree to sys.apth so that imports are working
#   alternative: add path to riotam_backend to the PYTHONPATH environment variable, but this includes one more step
#   which could be forget
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from drivers.adafruit_22_display.Display import Display
import json_keys as jk

# All API-functions need to accept json string request as argument and return a string as result


def get_display_state(request):
    return 'display state'


def set_display_state(request):

    display = Display()
    arguments = request[jk.REQUEST_KEY_ACTION_ARGUMENTS]

    if arguments == 'on':
        display.turn_on()
        return 'turned on display'

    elif arguments == 'off':
        display.turn_off()
        return 'turned off display'

    else:
        return 'invalid display state'


def get_display_intensity(request):
    return 'display intensity'


def set_display_intensity(request):

    display = Display()
    arguments = request[jk.REQUEST_KEY_ACTION_ARGUMENTS]

    try:
        intensity = int(arguments)
        display.set_intensity(intensity)
        return 'set display intensity to %d' % intensity

    except ValueError as e:
        return str(e)


def get_temperature(request):
    return 'temperature'


def get_humidity(request):
    return 'humidity'



