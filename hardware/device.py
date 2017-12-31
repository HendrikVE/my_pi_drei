#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

from __future__ import absolute_import, print_function, unicode_literals

from abc import ABC, abstractmethod

class Device(ABC):

    @abstractmethod
    def start_communication(self):
        pass

    @abstractmethod
    def stop_communication(self):
        pass

    @abstractmethod
    def request(self, method, argument):
        pass
