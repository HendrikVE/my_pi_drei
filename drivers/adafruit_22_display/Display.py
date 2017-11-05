#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen
from threading import Timer


class Display(object):

    _display_is_on = True
    _intensity = 700

    _screensaver_timeout = 0
    _screensaver_timer = None

    def __init__(self):
        Popen(["gpio", "-g", "mode", "18", "pwm"])
        self.set_intensity(self._intensity)

    def turn_off(self):
        old_intensity = self._intensity
        self.set_intensity(0)
        self._intensity = old_intensity
        self._display_is_on = False

    def turn_on(self):
        self.set_intensity(self._intensity)
        self._display_is_on = True

    def is_display_on(self):
        return self._display_is_on

    def set_intensity(self, intensity):

        if intensity < 0 or intensity > 1023:
            raise ValueError("intensity needs to be between 0 and 1023")

        self._intensity = intensity
        process = Popen(["gpio", "-g", "pwm", "18", str(intensity)])
        # wait for it to finish
        process.communicate()

    def set_screensaver_timeout(self, timeout):

        self._screensaver_timeout = timeout

        if self._screensaver_timer is not None:
            self._screensaver_timer.cancel()

        if timeout > 0:
            self._screensaver_timer = Timer(timeout, self.turn_off())

    def restart_screensaver_timer(self):
        self.set_screensaver_timeout(self._screensaver_timeout)
