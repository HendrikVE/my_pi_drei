#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import cgi
from Display import Display

form = cgi.FieldStorage()

action = form.getfirst('action')

print ('Content-Type: text/html')
print ('\n\r')

print('action = ' + action)

display = Display()
if action == "1":
    display.turn_on()
    print('display turned on')
elif action == "2":
    display.turn_off()
    print('display turned off')
