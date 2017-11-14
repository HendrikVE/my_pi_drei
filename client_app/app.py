#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# needs to be run as sudo to enable reboot and shutdown commands

from __future__ import print_function

import logging
import os
import signal
import sys
import termios
import tty
from getpass import getpass

# append root of the python code tree to sys.apth so that imports are working
#   alternative: add path to riotam_backend to the PYTHONPATH environment variable, but this includes one more step
#   which could be forget
from subprocess import Popen

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from drivers.adafruit_22_display.Display import Display
from drivers.dht22.DHT22 import DHT22
from menu import Menu, MenuAction
from config import config

SCREENSAVER_TIMEOUT = 120.0

LOGFILE = 'app.log'

display = Display()
display.open()
display.set_screensaver_timeout(SCREENSAVER_TIMEOUT)

gpio_dht22 = 4
dht22 = DHT22(gpio_dht22)


def main(menu):

    signal.signal(signal.SIGINT, signal_handler)

    print_manual()

    while True:

        user_input = get_user_input(display.restart_screensaver_timer, '> ')

        try:
            selected_action = int(user_input)

            action_count = menu.get_action_count()
            if (selected_action >= 0) and (selected_action < action_count):

                try:
                    menu.execute_action(selected_action)

                except Exception as e:
                    print(str(e))

            else:
                print('invalid action')

        except ValueError:
            if user_input == 'exit':
                exit_program()

            elif user_input == 'help':
                print_manual()

            else:
                print('invalid action')
                continue


def signal_handler(signal_number, frame):
    # ignore
    pass


def print_manual():
    os.system('clear')
    print(menu)


def exit_program():
    password = 'dummy'
    user_input = getpass('Enter password: ')

    if user_input == password:
        display.close()
        sys.exit()

    else:
        print('Action denied')


def reboot_system():
    Popen(['reboot'])


def shutdown_system():
    Popen(['shutdown', '-h', '0'])


def set_display_intensity():

    user_input = get_user_input(display.restart_screensaver_timer, 'Enter intensity (0-1023): ')

    try:
        intensity = int(user_input)

        try:
            display.set_intensity(intensity)

        except Exception as e:
            print(str(e))

    except ValueError:
        print('not a valid number')


def get_user_input(after_input_func, prompt=''):

    allowed_keycodes = []
    allowed_keycodes.extend(range(ord('0'), ord('9')+1))    # numbers
    allowed_keycodes.extend(range(ord('A'), ord('Z')))      # uppercase letters
    allowed_keycodes.extend(range(ord('a'), ord('z')))      # lowercase letters
    allowed_keycodes.append(ord(' '))  # space
    allowed_keycodes.append(127)                            # backspace
    allowed_keycodes.append(13)                             # enter

    sys.stdout.write(prompt)

    user_input = []
    input_char = 'X'

    # enter has keycode 13
    while ord(input_char) != 13:

        # get single char, without the need to press enter for newline
        # http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            input_char = sys.stdin.read(1)

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        keycode = ord(input_char)
        if keycode in allowed_keycodes:

            if keycode == 13:
                if len(user_input) == 0:
                    # ignore empty input, change input_char, so the loop continues
                    input_char = 'X'
                else:
                    # print a newline on enter
                    sys.stdout.write('\n\r')
                    user_input.append(input_char)

            elif keycode == 127:

                # dont be able to remove prompt
                if len(user_input) > 0:
                    # space behind '\b' important to replace char with 'empty' one on terminal
                    # '\b' is moving cursor 1 step back
                    sys.stdout.write('\b \b')
                    user_input.pop()

            else:
                sys.stdout.write(input_char)
                user_input.append(input_char)

            sys.stdout.flush()

        after_input_func()

    return ''.join(user_input).strip()


if __name__ == '__main__':

    logging.basicConfig(filename=LOGFILE, format=config.LOGGING_FORMAT,
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

    try:
        menu = Menu()

        actions = [
            MenuAction('print help', print_manual),
            MenuAction('turn on display', display.turn_on),
            MenuAction('turn off display', display.turn_off),
            MenuAction('set display intensity', set_display_intensity),
            MenuAction('print temperature', output_string=dht22.get_temperature()),
            MenuAction('print humidity', output_string=dht22.get_humidity()),
            MenuAction('shutdown', shutdown_system),
            MenuAction('reboot', reboot_system),
            MenuAction('exit program', exit_program),
        ]

        menu.add_item_list(actions)

        main(menu)

    except Exception as e:
        logging.error(str(e), exc_info=True)
        print(str(e))
