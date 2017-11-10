#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import cgi

form = cgi.FieldStorage()

action = form.getfirst('action')

print ('Content-Type: text/html')
print ('\n\r')

print('action = ' + action)
