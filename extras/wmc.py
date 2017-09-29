#!/usr/bin/python3
# -*- coding: utf-8 -*-

import curses
import display
from display import Color
import game

#import area
#import random


def main(stdscr):
    d = display.Display(stdscr)
    g = game.Game(d)
    g.run()
    return 0


curses.wrapper(main)
