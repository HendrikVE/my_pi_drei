#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import argparse
import logging

from drivers.adafruit_22_display.Display import Display
from drivers.dht22.DHT22 import DHT22

display = Display()

gpio_dht22 = 4
dht22 = DHT22(gpio_dht22)

menu = """
0  turn on display
1  turn off display
"""

# key: (function_to_execute, output_string)
menu_actions = {0: (display.turn_on, "display on"),
                1: (display.turn_off, "display off")}


def main():

    print(menu)

    while True:

        selected_action = int(input("> "))

        action = menu_actions[selected_action]
        execute_action(action)


def execute_action(action):

    action_method = action[0]
    action_method()

    action_text = action[1]
    print(action_text)


if __name__ == "__main__":

    #logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
    #                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        #logging.error(str(e), exc_info=True)
        print(str(e))