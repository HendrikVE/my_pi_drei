#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

# append root of the python code tree to sys.apth so that imports are working
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from hardware.adafruit_22_display.Display import Display
import api_json_keys as jk


def __json_result_template__():

    # insert only mandatory attributes here
    json_result = {
        jk.RESULT_KEY_RESULT: None,
        jk.RESULT_KEY_ERROR: None,
    }

    return json_result


########################################################################################################################
# All API-functions need to accept json string request as argument and return a string as result.                      #
#                                                                                                                      #
#                                                                                                                      #
# Create a new api-function with the following template:                                                               #
#                                                                                                                      #
# def get_temperature(request):                                                                                        #
#     json_result = __json_result_template__()                                                                         #
#                                                                                                                      #
#     # try-except-block only needed if REQUEST_KEY_ACTION_ARGUMENTS index is needed                                   #
#     try:                                                                                                             #
#         arguments = request[jk.REQUEST_KEY_ACTION_ARGUMENTS]                                                         #
#                                                                                                                      #
#     except KeyError:                                                                                                 #
#         json_result[jk.RESULT_KEY_ERROR] = 'missing %s' % jk.REQUEST_KEY_ACTION_ARGUMENTS                            #
#         return json_result                                                                                           #
#                                                                                                                      #
#     # your code here                                                                                                 #
#                                                                                                                      #
#     return json_result                                                                                               #
#                                                                                                                      #
########################################################################################################################


def get_display_state(request):
    json_result = __json_result_template__()

    dummy_state = 'off'
    json_result[jk.RESULT_KEY_RESULT] = dummy_state

    return json_result


def set_display_state(request):
    json_result = __json_result_template__()

    display = Display()

    try:
        argument = request[jk.REQUEST_KEY_ACTION_ARGUMENT]

    except KeyError:
        json_result[jk.RESULT_KEY_ERROR] = 'missing key %s' % jk.REQUEST_KEY_ACTION_ARGUMENT
        return json_result

    if argument == 'on':
        display.turn_on()
        json_result[jk.RESULT_KEY_RESULT] = 'turned on display'

    elif argument == 'off':
        display.turn_off()
        json_result[jk.RESULT_KEY_RESULT] = 'turned off display'

    else:
        json_result[jk.RESULT_KEY_ERROR] = 'invalid argument: %s' % argument
        return json_result

    return json_result


def get_display_intensity(request):
    json_result = __json_result_template__()

    dummy_intensity = 1000
    json_result[jk.RESULT_KEY_RESULT] = dummy_intensity

    return json_result


def set_display_intensity(request):
    json_result = __json_result_template__()

    display = Display()

    try:
        argument = request[jk.REQUEST_KEY_ACTION_ARGUMENT]

    except KeyError:
        json_result[jk.RESULT_KEY_ERROR] = 'missing key %s' % jk.REQUEST_KEY_ACTION_ARGUMENT
        return json_result

    try:
        intensity = int(argument)
        display.set_intensity(intensity)
        json_result[jk.RESULT_KEY_RESULT] = 'set display intensity to %d' % intensity

    except ValueError as e:
        json_result[jk.RESULT_KEY_ERROR] = str(e)

    return json_result


def get_temperature(request):
    json_result = __json_result_template__()

    try:
        argument = request[jk.REQUEST_KEY_ACTION_ARGUMENT]

    except KeyError:
        json_result[jk.RESULT_KEY_ERROR] = 'missing key %s' % jk.REQUEST_KEY_ACTION_ARGUMENT
        return json_result

    if argument == 'celsius':
        temperature = 21.0

    elif argument == 'fahrenheit':
        temperature = 42.0

    else:
        json_result[jk.RESULT_KEY_ERROR] = 'invalid argument: %s' % argument
        return json_result

    json_result[jk.RESULT_KEY_RESULT] = temperature

    return json_result


def get_humidity(request):
    json_result = __json_result_template__()

    humidity = 25
    json_result[jk.RESULT_KEY_RESULT] = humidity

    return json_result
