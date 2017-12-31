#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging
import time
import os
import sys
import zmq

# append root of the python code tree to sys.apth so that imports are working
CUR_DIR = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from hardware.arduino_nano.arduino_nano import ArduinoNano
from hardware.driver_process import DriverProcess

PORT = 7000
ADDRESS = 'tcp://127.0.0.1:%i' % PORT

_ERROR = 'error'
_RESULT = 'result'
_METHOD = 'method'


def main():
    """
    Run the Driver Process (operating as server)

    """
    print('starting arduino driver...')
    arduino_nano = ArduinoNano()
    driver_process = DriverProcess(ADDRESS, arduino_nano)

    while True:
        try:
            arduino_nano.start_communication()
            # established connection, break out of loop
            break

        except KeyboardInterrupt:
            sys.exit()

        except Exception:
            # retry connection in 1 second
            time.sleep(1)
            continue

    driver_process.run()


if __name__ == '__main__':
    main()