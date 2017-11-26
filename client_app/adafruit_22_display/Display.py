#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from subprocess import Popen
from threading import Timer


class DisplayAction:
    NONE, MANUAL_ON, MANUAL_OFF, SCREENSAVER_OFF = range(4)


class Display(object):

    _intensity = 700
    _last_display_action = DisplayAction.NONE

    _screensaver_timeout = 0.0
    _screensaver_timer = None

    def open(self):
        Popen(['gpio', '-g', 'mode', '18', 'pwm'])
        self.set_intensity(self._intensity)

    def close(self):

        # disable screensaver thread and turn on display
        self.set_screensaver_timeout(0)
        self.turn_on()

    def turn_off(self):

        old_intensity = self._intensity
        self.set_intensity(0)
        self._intensity = old_intensity
        self._last_display_action = DisplayAction.MANUAL_OFF

    def _turn_off_by_screensaver(self):

        if self._last_display_action == DisplayAction.MANUAL_OFF:
            return

        self.turn_off()
        self._last_display_action = DisplayAction.SCREENSAVER_OFF

    def turn_on(self):

        self.set_intensity(self._intensity)
        self.start_screensaver_timer()
        self._last_display_action = DisplayAction.MANUAL_ON

    def set_intensity(self, intensity):

        if intensity < 0 or intensity > 1023:
            raise ValueError('intensity needs to be between 0 and 1023')

        self._intensity = intensity
        process = Popen(['gpio', '-g', 'pwm', '18', str(intensity)])
        # wait for it to finish
        process.communicate()

    def start_screensaver_timer(self):

        if self._screensaver_timer is not None:
            self._screensaver_timer.cancel()

        if self._screensaver_timeout > 0:
            self._screensaver_timer = Timer(self._screensaver_timeout, self._turn_off_by_screensaver)
            self._screensaver_timer.start()

    def set_screensaver_timeout(self, timeout):

        self._screensaver_timeout = timeout

        if self._screensaver_timer is not None:
            self._screensaver_timer.cancel()

        self.start_screensaver_timer()

    def restart_screensaver_timer(self):

        if self._last_display_action == DisplayAction.MANUAL_OFF:
            return

        self.turn_on()
        self.set_screensaver_timeout(self._screensaver_timeout)
