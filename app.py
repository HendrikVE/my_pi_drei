#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import logging

import os
import tty
from getpass import getpass

import signal

import sys
from threading import Timer

import termios

from menu import Menu, MenuAction
from drivers.adafruit_22_display.Display import Display
from drivers.dht22.DHT22 import DHT22

SCREENSAVER_TIMEOUT = 5.0

display = Display()
display.set_screensaver_timeout(SCREENSAVER_TIMEOUT)

gpio_dht22 = 4
dht22 = DHT22(gpio_dht22)


def main(menu):

    #signal.signal(signal.SIGINT, signal_handler)

    print_manual()

    while True:

        user_input = get_user_input(display.restart_screensaver_timer, "> ")

        try:
            selected_action = int(user_input)

            action_count = menu.get_action_count()
            if (selected_action >= 0) and (selected_action < action_count):

                try:
                    menu.execute_action(selected_action)

                except Exception as e:
                    print(str(e))

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


def signal_handler(signal_number, frame):
    # ignore
    pass


def print_manual():
    os.system("clear")
    print(menu)


def exit_program():
    password = "dummy"
    user_input = getpass("Enter password: ")

    if user_input == password:

        # disable screensaver thread and turn on display
        display.set_screensaver_timeout(0)
        display.turn_on()

        sys.exit()

    else:
        print("Action denied")


def set_display_intensity():

    user_input = get_user_input(display.restart_screensaver_timer, "Enter intensity (0-1023): ")

    try:
        intensity = int(user_input)

        try:
            display.set_intensity(intensity)

        except Exception as e:
            print(str(e))

    except ValueError:
        print("not a valid number")


def get_user_input(after_input_func, prompt=""):

    sys.stdout.write(prompt)

    user_input = []
    input_char = -1

    # enter has keycode 10
    while ord(input_char) != 10:

        # get single char, without the need to press enter for newline
        # http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            input_char = sys.stdin.read(1)
            sys.stdout.write(input_char)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        after_input_func()

        user_input.append(input_char)

    return "".join(user_input).strip()


if __name__ == "__main__":

    #logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
    #                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

    try:
        menu = Menu()

        actions = [
            MenuAction("print help", print_manual),
            MenuAction("turn on display", display.turn_on),
            MenuAction("turn off display", display.turn_off),
            MenuAction("set display intensity", set_display_intensity),
            MenuAction("print temperature", None, dht22.get_temperature()),
            MenuAction("print humidity", None, dht22.get_humidity()),
            MenuAction("exit program", exit_program),
        ]

        menu.add_item_list(actions)

        main(menu)

    except Exception as e:
        #logging.error(str(e), exc_info=True)
        print(str(e))
