#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from subprocess import Popen
from threading import Timer

# append root of the python code tree to sys.apth so that imports are working
CUR_DIR = os.path.abspath(os.path.dirname(__file__))

PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from hardware.device import Device


class DisplayAction:
    NONE, MANUAL_ON, MANUAL_OFF, SCREENSAVER_OFF = range(4)


class RequestData:
    """
    Requests for the device

    """
    TURN_ON = 'turn_on'
    TURN_OFF = 'turn_off'
    SET_INTENSITY = 'set_intensity'
    START_SCREENSAVER_TIMER = 'start_screensaver_timer'
    SET_SCREENSAVER_TIMEOUT = 'set_screensaver_timeout'
    RESTART_SCREENSAVER_TIMER = 'restart_screensaver_timer'
    SHOW_IMAGE = 'show_image'


class Display(Device):

    _intensity = 700
    _last_display_action = DisplayAction.NONE

    _screensaver_timeout = 0.0
    _screensaver_timer = None

    # @override
    def start_communication(self):
        self.open()

    # @override
    def stop_communication(self):
        pass

    # @override
    def request(self, method, argument):
        """
        Requesting driver process

        Parameters
        ----------
        method : RequestData
            String for identifying an action to be requested
        """

        if method == RequestData.TURN_ON:
            self.turn_on()
            return None

        elif method == RequestData.TURN_OFF:
            self.turn_off()
            return None

        elif method == RequestData.SET_INTENSITY:
            return None

        elif method == RequestData.START_SCREENSAVER_TIMER:
            self.start_screensaver_timer()
            return None

        elif method == RequestData.SET_SCREENSAVER_TIMEOUT:
            return None

        elif method == RequestData.RESTART_SCREENSAVER_TIMER:
            self.restart_screensaver_timer()
            return None

        elif method == RequestData.SHOW_IMAGE:
            return None

        raise Exception('invalid method: %s' % method)

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

    def show_image(self, image_path):
        command = 'fbi -T 2 -d /dev/fb1 -noverbose -a %s' % os.path.abspath(image_path)
        Popen(command, shell=True)
