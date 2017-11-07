#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen
from threading import Timer


class Display(object):

    _intensity = 700

    _screensaver_timeout = 0.0
    _screensaver_timer = None

    def __init__(self):
        Popen(["gpio", "-g", "mode", "18", "pwm"])
        self.set_intensity(self._intensity)

    def turn_off(self):
        old_intensity = self._intensity
        self.set_intensity(0)
        self._intensity = old_intensity

    def turn_on(self):
        self.set_intensity(self._intensity)

        self.start_screensaver_timer()

    def set_intensity(self, intensity):

        if intensity < 0 or intensity > 1023:
            raise ValueError("intensity needs to be between 0 and 1023")

        self._intensity = intensity
        process = Popen(["gpio", "-g", "pwm", "18", str(intensity)])
        # wait for it to finish
        process.communicate()

    def start_screensaver_timer(self):

        if self._screensaver_timer is not None:
            self._screensaver_timer.cancel()

        if self._screensaver_timeout > 0:
            self._screensaver_timer = Timer(self._screensaver_timeout, self.turn_off)
            self._screensaver_timer.start()

    def set_screensaver_timeout(self, timeout):

        self._screensaver_timeout = timeout

        if self._screensaver_timer is not None:
            self._screensaver_timer.cancel()

        self.start_screensaver_timer()

    def restart_screensaver_timer(self):
        self.turn_on()
        self.set_screensaver_timeout(self._screensaver_timeout)
