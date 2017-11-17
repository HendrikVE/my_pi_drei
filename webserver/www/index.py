#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import textwrap

print('Content-Type: text/html')
print('\n\r')

print (textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                
                <title>RIOT OS App Market</title>
            </head>

            <body>
                
                <p>Welcome on the MyPiDrei-API. See information about the project <a href="https://github.com/HendrikVE/my_pi_drei">on GitHub</a></p>

            </body>
        </html>
    """))
