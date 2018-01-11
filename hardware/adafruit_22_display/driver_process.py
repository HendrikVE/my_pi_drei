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

from hardware.adafruit_22_display.display import Display
from hardware.driver_process import DriverProcess

ADDRESS = ('localhost', 7001)

SCREENSAVER_TIMEOUT = 120.0


def main():
    """
    Run the Driver Process (operating as server)

    """
    print('starting display driver...')

    display = Display()
    display.set_screensaver_timeout(SCREENSAVER_TIMEOUT)
    
    display.start_communication()

    driver_process = DriverProcess(ADDRESS, display)
    driver_process.run()


if __name__ == '__main__':
    main()