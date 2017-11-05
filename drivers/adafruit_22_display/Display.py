#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen


class Display(object):

    _intensity = 700

    def __init__(self):
        Popen(["gpio", "-g", "mode", "18", "pwm"])
        self.set_intensity(self._intensity)

    def turn_off(self):
        old_intensity = self._intensity
        self.set_intensity(0)
        self._intensity = old_intensity

    def turn_on(self):
        self.set_intensity(self._intensity)

    def set_intensity(self, intensity):

        if intensity < 0 or intensity > 1023:
            raise ValueError("intensity needs to be between 0 and 1023")

        self._intensity = intensity
        process = Popen(["gpio", "-g", "pwm", "18", str(intensity)])
        # wait for it to finish
        process.communicate()
