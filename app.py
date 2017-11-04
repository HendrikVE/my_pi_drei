#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import argparse
import logging

import Menu
from drivers.adafruit_22_display.Display import Display
from drivers.dht22.DHT22 import DHT22

display = Display()

gpio_dht22 = 4
dht22 = DHT22(gpio_dht22)

menu = Menu.Menu()

actions = [
    Menu.MenuAction("print help", "", menu.print_manual),
    Menu.MenuAction("turn on display", "display on", display.turn_on),
    Menu.MenuAction("turn off display", "display off", display.turn_off),
    Menu.MenuAction("exit program", "exit", exit),
]

menu.add_item_list(actions)


def main():

    print(menu)

    while True:

        try:
            selected_action = int(input("> "))

        except ValueError:
            # could not cast to int
            continue

        action_count = menu.get_action_count()
        if (selected_action >= 0) and (selected_action < action_count):
            menu.execute_action(selected_action)

        else:
            print("invalid action")


if __name__ == "__main__":

    #logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
    #                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        #logging.error(str(e), exc_info=True)
        print(str(e))