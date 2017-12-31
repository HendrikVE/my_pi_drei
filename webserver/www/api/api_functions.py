#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

# append root of the python code tree to sys.apth so that imports are working
CUR_DIR = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from hardware.driver_process import RequestDriverProcess
from arduino.dht22.dht22_interface import RequestData
from .api_json_keys import *

API_VERSION = '0.1'


def __json_result_template__():

    # insert only mandatory attributes here
    json_result = {
        RESULT_KEY_API_VERSION: API_VERSION,
        RESULT_KEY_RESULT: None,
        RESULT_KEY_ERROR: None,
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


def get_temperature(request):
    json_dict = __json_result_template__()

    port = 7000
    address = 'tcp://127.0.0.1:%i' % port
    rdp = RequestDriverProcess(address)

    try:
        argument = request[REQUEST_KEY_ACTION_ARGUMENT]

    except KeyError:
        json_dict[RESULT_KEY_ERROR] = 'missing key %s' % REQUEST_KEY_ACTION_ARGUMENT
        return json_dict

    if argument == 'celsius':
        try:
            temperature = rdp.request(RequestData.TEMP_CEL)
        except Exception as e:
            json_dict[RESULT_KEY_ERROR] = str(e)
            return json_dict

    elif argument == 'fahrenheit':
        try:
            temperature = rdp.request(RequestData.TEMP_FAH)
        except Exception as e:
            json_dict[RESULT_KEY_ERROR] = str(e)
            return json_dict

    else:
        json_dict[RESULT_KEY_ERROR] = 'invalid argument: %s' % argument
        return json_dict

    json_dict[RESULT_KEY_RESULT] = temperature

    return json_dict


def get_heat_index(request):
    json_dict = __json_result_template__()

    port = 7000
    address = 'tcp://127.0.0.1:%i' % port
    rdp = RequestDriverProcess(address)

    try:
        argument = request[REQUEST_KEY_ACTION_ARGUMENT]

    except KeyError:
        json_dict[RESULT_KEY_ERROR] = 'missing key %s' % REQUEST_KEY_ACTION_ARGUMENT
        return json_dict

    if argument == 'celsius':
        try:
            heat_index = rdp.request(RequestData.HEAT_INDEX_CEL)
        except Exception as e:
            json_dict[RESULT_KEY_ERROR] = str(e)
            return json_dict

    elif argument == 'fahrenheit':
        try:
            heat_index = rdp.request(RequestData.HEAT_INDEX_FAH)
        except Exception as e:
            json_dict[RESULT_KEY_ERROR] = str(e)
            return json_dict

    else:
        json_dict[RESULT_KEY_ERROR] = 'invalid argument: %s' % argument
        return json_dict

    json_dict[RESULT_KEY_RESULT] = heat_index

    return json_dict


def get_humidity(request):
    json_dict = __json_result_template__()

    port = 7000
    address = 'tcp://127.0.0.1:%i' % port
    rdp = RequestDriverProcess(address)

    try:
        humidity = rdp.request(RequestData.HUMIDITY)
    except Exception as e:
        json_dict[RESULT_KEY_ERROR] = str(e)
        return json_dict

    json_dict[RESULT_KEY_RESULT] = humidity

    return json_dict
