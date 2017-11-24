#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import serial
import time

s = serial.Serial('/dev/ttyUSB0', 9600) # change name if needed
try:
    s.open()
except:
    pass
time.sleep(5) # wait for the arduino to reset after serial connection

while True:
    try:
        while True:
            response = s.readline()
            print(response)
    except KeyboardInterrupt:
        s.close()
