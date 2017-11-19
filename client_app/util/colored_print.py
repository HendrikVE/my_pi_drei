#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import sys

RED = '\033[1;31m'
BLUE = '\033[1;34m'
CYAN = '\033[1;36m'
GREEN = '\033[0;32m'
YELLOW = '\[\033[1;33m\]'

BOLD = '\033[;1m'
REVERSE = '\033[;7m'

RESET = '\033[0;0m'


def styled_text(text, color):
    return color + text + RESET


def print_red(output_string):
    _colored_print(output_string, RED)


def print_blue(output_string):
    _colored_print(output_string, BLUE)


def print_cyan(output_string):
    _colored_print(output_string, CYAN)


def print_green(output_string):
    _colored_print(output_string, GREEN)


def print_bold(output_string):
    _colored_print(output_string, BOLD)


def print_reverse(output_string):
    _colored_print(output_string, REVERSE)


def _colored_print(output_string, style):
    sys.stdout.write(style)
    sys.stdout.write(output_string)
    print(RESET)
