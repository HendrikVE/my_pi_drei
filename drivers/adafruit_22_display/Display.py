#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen

class Display(object):

    _intensity = 700

    def init(self):
        Popen(["gpio", "-g", "mode", "18", "pwm"])
        self.set_intensity(self._intensity)

    def turn_off(self):
        old_intensity = self._intensity
        self.set_intensity(0)
        self._intensity = old_intensity

    def turn_on(self):
        self.set_intensity(self._intensity)

    def set_intensity(self, intensity):
        self._intensity = intensity
        Popen(["gpio", "-g", "pwm", "18", str(intensity)])
