#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

# needs to be run as sudo to enable reboot and shutdown commands

from __future__ import absolute_import, print_function, unicode_literals

import logging
import os
import signal
import sys
import termios
import tty
from getpass import getpass
from subprocess import Popen, PIPE
import time

# append root of the python code tree to sys.apth so that imports are working
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CLIENT_APP_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR))

PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

from hardware.driver_process import RequestDriverProcess
from arduino.dht22.dht22_interface import RequestData
from config import config
from client_app.menu import Menu, MenuAction, ExitMenuException, Submenu
import client_app.util.colored_print as cp

SCREENSAVER_TIMEOUT = 120.0

LOGFILE = os.path.join(CLIENT_APP_ROOT_DIR, 'log', 'app.log')

PORT_DHT22 = 7000
ADDRESS_DHT22 = 'tcp://127.0.0.1:%i' % PORT_DHT22

display = Display()
display.open()
display.set_screensaver_timeout(SCREENSAVER_TIMEOUT)


def main():

    signal.signal(signal.SIGINT, signal_handler)

    menu = Menu()

    def print_manual_wrapper():
        print_manual(menu)

    actions = [
        # EXIT PROGRAM
        MenuAction('exit program', exit_program),

        # MANUAL
        MenuAction('print help', print_manual_wrapper),

        # OVERVIEW
        MenuAction('overview', show_overview),

        # DISPLAY ACTIONS SUBMENU
        MenuAction('display', lambda previous_menu=menu: open_display_submenu(previous_menu)),

        # SYSTEM ACTIONS SUBMENU
        MenuAction('system', lambda previous_menu=menu: open_system_submenu(previous_menu)),
    ]

    menu.add_item_list(actions)

    menu_handler(None, menu)


def menu_handler(previous_menu, menu):

    print_manual(menu)

    while True:

        user_input = get_user_input(display.restart_screensaver_timer, '> ')

        try:
            selected_action = int(user_input)

            action_count = menu.get_action_count()
            if (selected_action >= 0) and (selected_action < action_count):

                try:
                    menu.execute_action(selected_action)

                except ExitMenuException:
                    if previous_menu is not None:
                        # reprint manual (entering previous menu)
                        print_manual(previous_menu)
                    # finish infinite loop
                    break

                except Exception as e:
                    print(str(e))

            else:
                print('invalid action')

        # 'text' area
        except ValueError:
            if user_input == 'exit':
                exit_program()

            elif user_input == 'help':
                print_manual(menu)

            else:

                matched_action = None

                for action in menu.get_actions():
                    if user_input == action.get_name():
                        matched_action = action
                        break

                if matched_action is not None:
                    try:
                        matched_action.execute()

                    except ExitMenuException:
                        if previous_menu is not None:
                            # reprint manual (entering previous menu)
                            print_manual(previous_menu)
                        # finish infinite loop
                        break

                else:
                    # no match found
                    print('invalid action')
                    continue


def signal_handler(signal_number, frame):
    # ignore
    pass


def print_manual(menu):
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


def update_system():

    process = Popen(['apt-get update && apt-get dist-upgrade -y'], stdout=PIPE, shell=True)

    while True:
        output = process.stdout.readline()

        if output == '' and process.poll() is not None:
            break

        if output:
            print(output.strip())

        process.poll()


def open_system_submenu(current_menu):

    submenu = Submenu()

    actions = [
        # MANUAL
        MenuAction('print help', lambda menu=submenu: print_manual(menu)),

        # SYSTEM ACTIONS
        MenuAction('update', update_system),
        MenuAction('shutdown', shutdown_system),
        MenuAction('reboot', reboot_system),
    ]

    submenu.add_item_list(actions)

    menu_handler(current_menu, submenu)


def open_display_submenu(current_menu):

    submenu = Submenu()

    actions = [
        # MANUAL
        MenuAction('print help', lambda menu=submenu: print_manual(menu)),

        # DISPLAY
        MenuAction('turn on', display.turn_on),
        MenuAction('turn off', display.turn_off),
        MenuAction('set intensity', set_display_intensity),
    ]

    submenu.add_item_list(actions)

    menu_handler(current_menu, submenu)


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


def show_overview():

    def styled_temperature_string(temperature):

        temperature_string = '%i °C' % temperature

        if temperature <= 0:
            return cp.style_text(temperature_string, cp.BLUE_LIGHT)

        elif temperature <= 30:
            return cp.style_text(temperature_string, cp.WHITE)

        else:
            return cp.style_text(temperature_string, cp.RED)

    def styled_humidity_string(humidity):

        humidity_string = '%i %%' % humidity

        if humidity <= 55:
            return cp.style_text(humidity_string, cp.WHITE)

        else:
            return cp.style_text(humidity_string, cp.BLUE_LIGHT)

    rdp = RequestDriverProcess(ADDRESS_DHT22)

    while True:
        try:
            try:
                temperature = rdp.request(RequestData.TEMP_CEL)
            except Exception:
                temperature = None

            try:
                heat_index = rdp.request(RequestData.HEAT_INDEX_CEL)
            except Exception:
                heat_index = None

            try:
                humidity = rdp.request(RequestData.HUMIDITY)
            except Exception:
                humidity = None

            temperature_string = cp.style_text('NaN  ', cp.RED) if temperature is None else styled_temperature_string(int(temperature))
            heat_index_string = cp.style_text('NaN  ', cp.RED) if heat_index is None else styled_temperature_string(int(heat_index))
            humidity_string = cp.style_text('NaN ', cp.RED) if humidity is None else styled_humidity_string(int(humidity))

            print('')
            print('########################################')
            print('#                                      #')
            print('# SYSTEM STATUS                        #')
            print('# ip                  ' + cp.style_text('192.168.2.114', cp.WHITE) + '    #')
            print('# apache running      ' + cp.style_text('yes', cp.GREEN) + '              #')
            print('# cpu load            ' + cp.style_text('32 %', cp.YELLOW) + '             #')
            print('# free memory         ' + cp.style_text('954 MB', cp.WHITE) + '           #')
            print('# uptime              ' + cp.style_text('00:17:07', cp.WHITE) + '         #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('#                                      #')
            print('# DISPLAY                              #')
            print('# intensity           ' + cp.style_text('700', cp.WHITE) + '              #')
            print('#                                      #')
            print('# SENSORS                              #')
            print('# temperature:        ' + temperature_string + '            #')
            print('# humidity:           ' + humidity_string + '             #')
            print('#                                      #')
            print('# heat index          ' + heat_index_string + '            #')
            print('#                                      #')
            print('########################################')

            time.sleep(2)

        except KeyboardInterrupt:
            break

        except Exception as e:
            logging.error(str(e), exc_info=True)
            break


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
        main()

    except Exception as e:
        logging.error(str(e), exc_info=True)
        print(str(e))
