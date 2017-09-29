# -*- coding: utf-8 -*-

import curses
from enum import IntEnum


class Color(IntEnum):
    """Enumeration of valid colors."""

    DarkBlack = 0
    DarkRed = 1
    DarkGreen = 2
    DarkYellow = 3
    DarkBlue = 4
    DarkMagenta = 5
    DarkCyan = 6
    DarkWhite = 7
    Black = 8
    Red = 9
    Green = 10
    Yellow = 11
    Blue = 12
    Magenta = 13
    Cyan = 14
    White = 15

    PitchBlack = DarkBlack
    Blood = DarkRed
    Pine = DarkGreen
    Brown = DarkYellow
    Indigo = DarkBlue
    Metal = DarkCyan
    Purple = DarkMagenta
    Gray = DarkWhite


class Key(IntEnum):
    """Enumeration of keypress codes"""
    Up = curses.KEY_UP
    Down = curses.KEY_DOWN
    Left = curses.KEY_LEFT
    Right = curses.KEY_RIGHT
    Up2 = ord('8')
    Down2 = ord('2')
    Left2 = ord('4')
    Right2 = ord('6')
    UpLeft = 262
    UpRight = 339
    DownLeft = 360
    DownRight = 338
    UpLeft2 = ord('7')
    UpRight2 = ord('9')
    DownLeft2 = ord('1')
    DownRight2 = ord('3')
    Center = ord('5')
    Center2 = 350
    Dot = ord('.')
    Dot2 = 330
    Escape = 27
    ResizeDisplay = curses.KEY_RESIZE


class Display:
    """Class, displaying characters on screen using curses and reading input."""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(False)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def pair_attr(self, color, atrs):
        atr = curses.A_BOLD
        if 'r' in atrs:
            atr |= curses.A_REVERSE
        if 'b' in atrs:
            atr &= ~curses.A_BOLD
        if 'l' in atrs:
            atr |= curses.A_BLINK
        if 'u' in atrs:
            atr |= curses.A_UNDERLINE

        if color < 0 or color > 15:
            return (0, 0)
        elif color < 8:
            return (color + 1, atr | curses.A_DIM)
        else:
            return (color - 8 + 1, atr)

    def size(self):
        y, x = self.stdscr.getmaxyx()
        return (x, y)

    def prn(self, x, y, text, color=-1, atrs=''):
        """Print text on the screen.

        Prints 'text' at position 'x, y' with optional color
        (see Color enum) and a string of attributes.

        Attributes allowed:
        r = reversed;
        b = toggle bold;
        l = blinking;
        u = underlined.

        Note, that symbols are bold by default
        """
        if color >= 0:
            pair, attr = self.pair_attr(color, atrs)
            self.stdscr.addstr(y, x, text, curses.color_pair(pair) | attr)
        else:
            self.stdscr.addstr(y, x, text)

    def pr(self, text, color=-1, atrs=''):
        """Print text on the screen.

        Just like prn, but text is printed at current cursor postion"""
        if color >= 0:
            pair, attr = self.pair_attr(color, atrs)
            self.stdscr.addstr(text, curses.color_pair(pair) | attr)
        else:
            self.stdscr.addstr(text)

    def move(self, x, y):
        self.stdscr.move(y, x)

    def input(self):
        return self.stdscr.getch()

    def pause(self, msec):
        self.stdscr.refresh()
        curses.delay_output(msec)
