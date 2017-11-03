#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time

from Display import Display

display = Display()
display.init()

display.turn_off()

time.sleep(3)

display.turn_on()
