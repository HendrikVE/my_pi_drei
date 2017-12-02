#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import print_function

import pygame

pygame.mixer.init()
pygame.mixer.music.load('/home/hendrik/07iDisco.mp3')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    continue