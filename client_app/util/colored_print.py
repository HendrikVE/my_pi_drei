#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

_RED = "\033[1;31m"
_BLUE = "\033[1;34m"
_CYAN = "\033[1;36m"
_GREEN = "\033[0;32m"
_RESET = "\033[0;0m"
_BOLD = "\033[;1m"
_REVERSE = "\033[;7m"


def print_red(output_string):
    _colored_print(output_string, _RED)


def print_blue(output_string):
    _colored_print(output_string, _BLUE)


def print_cyan(output_string):
    _colored_print(output_string, _CYAN)


def print_green(output_string):
    _colored_print(output_string, _GREEN)


def print_bold(output_string):
    _colored_print(output_string, _BOLD)


def print_reverse(output_string):
    _colored_print(output_string, _REVERSE)


def _colored_print(output_string, style):
    print(style)
    print(output_string)
    print(_RESET)
