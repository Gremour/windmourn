# -*- coding: utf-8 -*-

import pygame
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


class Window:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.size_x = 0
        self.size_y = 0
        self.pos_x = 0
        self.pos_y = 0


class Display:
    """Class, displaying characters on screen using pygame and reading input."""

    def __init__(self):
        scr_size = (1200, 800)
        fnt_size = 20
        fnt_name = 'DejaVuSansMono-Bold.ttf'
        fntb_name = 'DejaVuSansMono.ttf'
        self.stdscr = Window()

        pygame.init()
        pygame.key.set_repeat(400, 5)
        self.font = pygame.font.Font(fnt_name, fnt_size)
        self.fontb = pygame.font.Font(fntb_name, fnt_size)
        self.sym_x, self.sym_y = self.font.size('A')
        self.init_screen(scr_size)
        pygame.display.set_caption('Yet Another Crawler (unversioned)')
        icon = self.font.render('@', True, (255, 255, 255), (0, 0, 0))
        pygame.display.set_icon(icon)
        self.bg_color = Color.Black
        self.is_running = True

    def init_screen(self, scr_size):
        self.pix_x, self.pix_y = scr_size
        self.stdscr.size_x = self.pix_x // self.sym_x
        self.stdscr.size_y = self.pix_y // self.sym_y
        self.screen = pygame.display.set_mode(scr_size, pygame.RESIZABLE)
        #print('d/x{0}/y{1}'.format(self.stdscr.size_x, self.stdscr.size_y))

    def size(self, win=None):
        if win is None:
            win = self.stdscr
        return win.size_x, win.size_y

    def get_col_atr(self, color, atrs):
        fnt = self.font if not 'b' in atrs else self.fontb
        nfg = color if not 'r' in atrs else self.bg_color
        nbg = color if 'r' in atrs else self.bg_color
        colfg = color_dict[nfg] if nfg in color_dict else (127, 127, 127)
        colbg = color_dict[nbg] if nbg in color_dict else (0, 0, 0)
        return fnt, colfg, colbg

    def prn(self, text, x=None, y=None, color=None, atrs='', win=None):
        """Print text on the screen.

        Prints 'text' at position 'x, y' with optional color
        (see Color enum) and a string of attributes.

        Attributes allowed:
        r = reversed;
        b = toggle bold;
        l = blinking;
        u = underlined.

        * only 'rb' works ATM.

        Note, that symbols are bold by default
        """
        if win is None:
            win = self.stdscr
        if x is not None:
            win.pos_x = x
        if y is not None:
            win.pos_y = y
        if win.y + win.pos_y not in range (self.stdscr.y, self.stdscr.y + self.stdscr.size_y) or \
           win.pos_y not in range(0, win.size_y):
            return
        fnt, colfg, colbg = self.get_col_atr(color, atrs)
        for sym in text:
            if win.x + win.pos_x in range(self.stdscr.x, self.stdscr.x + self.stdscr.size_x) and \
               win.pos_x in range(0, win.size_x):
                ssurf = fnt.render(sym, True, colfg, colbg)
                self.screen.blit(ssurf, ((win.x + win.pos_x) * self.sym_x,
                                         (win.y + win.pos_y) * self.sym_y))
            win.pos_x += 1

    def move(self, x, y, win=None):
        if win is None:
            win = self.stdscr
        win.pos_x, win.pos_y = x, y

    def input(self):
        self.refresh()
        key = None
        while key is None:
            #pygame.event.pump()
            #event = pygame.event.wait()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    key = Key.ResizeDisplay
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                elif event.type == pygame.VIDEORESIZE:
                    #print ('display resize {0}'.format((event.w, event.h)))
                    self.init_screen((event.w, event.h))
                    key = Key.ResizeDisplay
        #print ('key={0} {1}'.format(key, chr(key)))
        return key

    def fill(self, sym, x=None, y=None, w=None, h=None,
                   color=None, atrs='', win=None):
        if win is None:
            win = self.stdscr
        if x is None or y is None or w is None or h is None:
            x, y, w, h = 0, 0, win.size_x, win.size_y
        fnt, colfg, colbg = self.get_col_atr(color, atrs)
        ssurf = fnt.render(sym, True, colfg, colbg)
        for r in range(y, y + h):
            cy = win.y + r
            if cy not in range(self.stdscr.y, self.stdscr.y + self.stdscr.size_y):
                continue
            for c in range(x, x + w):
                cx = win.x + c
                if cx not in range(self.stdscr.x, self.stdscr.x + self.stdscr.size_x):
                    continue
                self.screen.blit(ssurf, (cx * self.sym_x,
                                         cy * self.sym_y))

    def pause(self, msec):
        pygame.time.delay(msec)

    def refresh(self):
        pygame.display.flip()
