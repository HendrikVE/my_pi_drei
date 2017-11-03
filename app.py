#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time

from drivers.adafruit_22_display.Display import Display
from drivers.dht22 import DHT22

display = Display()

while True:
    display.turn_on()
    time.sleep(1)

    display.turn_off()
    time.sleep(1)

    display.set_intensity(600)
    time.sleep(1)

    display.set_intensity(200)
    time.sleep(1)
