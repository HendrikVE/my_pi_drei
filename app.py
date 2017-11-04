#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import logging

import os
from getpass import getpass

import signal

import sys

from menu import Menu, MenuAction
from drivers.adafruit_22_display.Display import Display
from drivers.dht22.DHT22 import DHT22

display = Display()

gpio_dht22 = 4
dht22 = DHT22(gpio_dht22)


def print_manual():
    os.system("clear")
    print(menu)


def exit_program():
    password = "dummy"
    user_input = getpass("Enter password: ")

    if user_input == password:
        sys.exit()

    else:
        print("Action denied")


menu = Menu()

actions = [
    MenuAction("print help", print_manual),
    MenuAction("turn on display", display.turn_on, "display on"),
    MenuAction("turn off display", display.turn_off, "display off"),
    MenuAction("print temperature", None, dht22.get_temperature()),
    MenuAction("print humidity", None, dht22.get_humidity()),
    MenuAction("exit program", exit_program),
]

menu.add_item_list(actions)


def main():

    signal.signal(signal.SIGINT, signal_handler)

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
                exit_program()

            elif user_input == "help":
                print_manual()

            else:
                print("invalid action")
                continue


def signal_handler(signal, frame):
    # ignore
    pass


if __name__ == "__main__":

    #logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
    #                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        main()

    except Exception as e:
        #logging.error(str(e), exc_info=True)
        print(str(e))