# -*- coding: utf-8 -*-
# Values for colors, keys, directions, etc.

from enum import IntEnum

class Color(IntEnum):
    """Enumeration of valid colors."""
    Black = 0
    DarkRed = 1
    DarkGreen = 2
    DarkYellow = 3
    DarkBlue = 4
    DarkMagenta = 5
    DarkCyan = 6
    Gray = 7
    Dark = 8
    Red = 9
    Green = 10
    Yellow = 11
    Blue = 12
    Magenta = 13
    Cyan = 14
    White = 15

    Blood = 16
    OldBlood = 17
    Pine = 18
    Brown = 19
    Metal = 20
    Sky = 21
    Concrete = 23
    Skin = 22

    Weird = -1

color_dict = \
{
    Color.Weird: (64, 23, 12),
    Color.Black: (0, 0, 0),
    Color.DarkRed: (127, 0, 0),
    Color.DarkGreen: (0, 127, 0),
    Color.DarkYellow: (127, 127, 0),
    Color.DarkBlue: (0, 0, 127),
    Color.DarkMagenta: (127, 0, 127),
    Color.DarkCyan: (0, 127, 127),
    Color.Gray: (127, 127, 127),
    Color.Dark: (64, 63, 63),
    Color.Red: (255, 0, 0),
    Color.Green: (0, 255, 0),
    Color.Yellow: (255, 255, 0),
    Color.Blue: (0, 0, 255),
    Color.Magenta: (255, 0, 255),
    Color.Cyan: (0, 255, 255),
    Color.White: (255, 255, 255),
    Color.Blood: (200, 0, 23),
    Color.Pine: (23, 127, 63),
    Color.Brown: (127, 63, 0),
    Color.Metal: (130, 180, 210),
    Color.Sky: (200, 210, 210),
    Color.Concrete: (135, 135, 135),
    Color.Skin: (250, 180, 180),

}


class Key(IntEnum):
    """Enumeration of keypress codes"""
    Up = 264
    Down = 258
    Left = 260
    Right = 262
    UpLeft = 263
    UpRight = 265
    DownLeft = 257
    DownRight = 259
    Center = 261
    Dot = 266
    Escape = 27
    ResizeDisplay = 0
    Refresh = 114


class Dir(IntEnum):
    UpLeft = 0
    Up = 1
    UpRight = 2
    Left = 3
    Center = 4
    Right = 5
    DownLeft = 6
    Down = 7
    DownRight = 8


dir_dict = [ (-1, -1), (0, -1), (1, -1),
             (-1, 0),  (0, 0),  (1, 0),
             (-1, 1),  (0, 1),  (1, 1) ]


def key2dir(key):
    if key == Key.UpLeft:
        return Dir.UpLeft
    elif key == Key.Up:
        return Dir.Up
    elif key == Key.UpRight:
        return Dir.UpRight
    elif key == Key.Left:
        return Dir.Left
    elif key == Key.Center:
        return Dir.Center
    elif key == Key.Right:
        return Dir.Right
    elif key == Key.DownLeft:
        return Dir.DownLeft
    elif key == Key.Down:
        return Dir.Down
    elif key == Key.DownRight:
        return Dir.DownRight
    else:
        return None


endofstr = ('.', '!', '?')
vowels = ('a', 'e', 'i', 'o', 'u', 'y')
