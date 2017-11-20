#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import pygame
pygame.mixer.init()
pygame.mixer.music.load('/home/hendrik/07iDisco.mp3')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    continue