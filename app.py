#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import logging

import os

import Menu
from drivers.adafruit_22_display.Display import Display
from drivers.dht22.DHT22 import DHT22

display = Display()

gpio_dht22 = 4
dht22 = DHT22(gpio_dht22)

menu = Menu.Menu()

actions = [
    Menu.MenuAction("print help",        menu.print_manual),
    Menu.MenuAction("turn on display",   display.turn_on,    "display on"),
    Menu.MenuAction("turn off display",  display.turn_off,   "display off"),
    Menu.MenuAction("print temperature", None,               dht22.get_temperature()),
    Menu.MenuAction("print humidity",    None,               dht22.get_humidity()),
    Menu.MenuAction("exit program",      exit),
]

menu.add_item_list(actions)


def main():

    print(menu)

    while True:

        user_input = raw_input("> ")

        try:
            selected_action = int(user_input)

            action_count = menu.get_action_count()
            if (selected_action >= 0) and (selected_action < action_count):
                menu.execute_action(selected_action)

            else:
                print("invalid action")

        except ValueError:
            if user_input == "exit":
                exit()

            elif user_input == "help":
                os.system("clear")
                print(menu)

            else:
                print("invalid action")
                continue


if __name__ == "__main__":

    #logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
    #                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        #logging.error(str(e), exc_info=True)
        print(str(e))