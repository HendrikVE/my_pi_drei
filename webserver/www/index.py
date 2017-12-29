#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import textwrap

print('Content-Type: text/html')
print('\n\r')

print (textwrap.dedent("""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                
                <title>MyPiDrei API</title>
            </head>

            <body>
                
                <p>Welcome on the MyPiDrei API. See information about the project <a href="https://github.com/HendrikVE/my_pi_drei">on GitHub</a></p>

            </body>
        </html>
    """))
