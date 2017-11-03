#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen

class Display(object):

    _intensity = 0

    def init(self):
        Popen(["gpio", "-g", "mode", "18", "pwm"])

    def turn_off(self):
        self.set_intensity(0)

    def turn_on(self):
        self.set_intensity(700)

    def set_intensity(self, intensity):
        _intensity = intensity
        Popen(["gpio", "-g", "pwm", "18", str(intensity)])
