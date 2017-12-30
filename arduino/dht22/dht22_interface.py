#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

class TempScale:
    """
    Possible scale types for requesting temperatures

    """
    CELSIUS, FAHRENHEIT = range(2)


class RequestData:
    """
    Serial requests for the device (dependant on code of the arduino)

    """
    TEMP_CEL = 'temp_cel'
    TEMP_FAH = 'temp_fah'
    HEAT_INDEX_CEL = 'heat_index_cel'
    HEAT_INDEX_FAH = 'heat_index_fah'
    HUMIDITY = 'humidity'
