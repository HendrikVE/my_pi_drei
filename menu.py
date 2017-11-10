#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function


class Menu(object):

    _menu_actions = []

    def add_item(self, action):

        if type(action) is not MenuAction:
            raise TypeError('action needs to be of type MenuAction')

        self._menu_actions.append(action)

    def add_item_list(self, action_list):
        for action in action_list:
            self.add_item(action)

    def execute_action(self, index, print_output=True):

        if index >= len(self._menu_actions):
            raise IndexError

        self._menu_actions[index].execute(print_output)

    def get_action_count(self):
        return len(self._menu_actions)

    def __str__(self):

        menu_manual = []
        index = 0
        for action in self._menu_actions:

            menu_manual.append(str(index) + " ")
            menu_manual.append(action.get_name() + "\n")

            index += 1

        return "".join(menu_manual)


class MenuAction(object):

    _action_name = None
    _output_string = None
    _method = None

    def __init__(self, action_name, method, output_string=None):

        self._action_name = action_name
        self._output_string = output_string
        self._method = method

    def get_name(self):
        return self._action_name

    def execute(self, print_output=True):

        if self._method is not None:
            self._method()

        if print_output and (self._output_string is not None):
            print(self._output_string)
