# -*- coding: utf-8 -*-

from collections import deque
from modules.display import Color

endofstr = ('.', '!', '?')
vowels = ('a', 'e', 'i', 'o', 'u', 'y')

class Line:
    """Log's line consists of words and colors"""
    def __init__(self, text, def_color, colors=None):
        self.mul = 1
        self.def_color = def_color
        if text[-1] not in endofstr:
            text = text + '.'
        self.tokens = []
        ncol = 0
        cap_next = True
        colch = False
        word = ''
        for ch in text:
            if ch == '@' and not colch:
                colch = True
                continue
            if colch:
                colch = False
                if ch == '.':
                    ch = '@'
                elif ch == '+' or ch == '-':
                    color = self.def_color
                    if ch == '+' and colors is not None and ncol < len(colors):
                        color = colors[ncol]
                        ncol += 1
                    if len(word) > 0:
                        self.tokens += [word]
                        word = ''
                    self.tokens += [color]
                    continue

            word += ch if not cap_next else ch.upper()
            if ch != ' ':
                cap_next = False
            if ch in endofstr:
                cap_next = True
            if ch == ' ':
                self.tokens += [word]
                word = ''
        else:
            self.tokens += [word]

    def prn(self, d, win, y, test=False):
        phys_lines = 1
        total_phys_lines = 1
        if test is False:
            total_phys_lines = self.prn(d, win, y, True)
        pos_y = 0
        pos_x = 1
        color = self.def_color
        for token in self.tokens + ([Color.Dark, ' x{}'.format(self.mul)] if self.mul > 1 else []):
            tt = type(token)
            if tt is Color or tt is int:
                color = token
                continue
            elif tt is not str:
                raise TypeError
            l = len(token)
            if pos_x + l > win.size_x:
                pos_y += 1
                phys_lines += 1
                pos_x = 3
            if test is False:
                d.prn(token, pos_x, y - total_phys_lines + 1 + pos_y, color, win=win)
            pos_x += l
        return phys_lines

class Log:
    """Display game log messages."""
    max_lines = 32

    def __init__(self):
        self.lines = deque()
        self.default_color = Color.Gray
        self.symbol_color = Color.Dark

        # Index of messages of the latest turn
        self.fresh_index = -1

        # Index of the last line, that is displayed in log window
        self.cursor = -1

    def next_turn(self):
        self.fresh_index = len(self.lines)
        self.cursor = self.fresh_index - 1

    def add(self, text, colors=None):
        """This function adds a line into log.

        '@' symbols are replaced with color change command.
        Color is taken from tuple 'colors'.
        If tuple is shorter than number of '@' symbols, default log color will be used
        To print '@', double it ('@@')"""

        while len(self.lines) >= self.max_lines:
            self.lines.popleft()
            self.fresh_index -= 1
            self.cursor -= 1

        new_line = Line(text, self.default_color, colors)
        if len(self.lines) > 0 and new_line.tokens == self.lines[-1].tokens:
            self.lines[-1].mul += 1
            if self.fresh_index >= len(self.lines):
                self.fresh_index = len(self.lines) - 1
        else:
            self.lines.append(new_line)
        self.cursor = len (self.lines) - 1

    def prn(self, d, win):
        y = win.size_y - 1
        cur = self.cursor
        while y >= 0 and cur >= 0:
            log_sym = '+' if cur >= self.fresh_index else ' '
            printed = self.lines[cur].prn(d, win, y)
            cur -= 1
            y -= printed
            d.prn(log_sym, 0, y + 1, self.symbol_color, win=win)
