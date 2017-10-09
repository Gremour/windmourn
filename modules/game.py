# -*- coding: utf-8 -*-

from modules.log import Log
from modules.area import Area
from modules.actor import *
from modules.display import Key, Color, Window
from modules.terrain import reference

import random


class Game:
    """Our game state."""
    inf_x = 40
    inf_y = 12
    turn_len = 100
    vision_range = 10

    offmap_sym = ' '
    offmap_color = Color.Gray

    def __init__(self, display):
        self.d = display
        self.key = 32
        self.wmap = Window()
        self.wstat = Window()
        self.wlog = Window()
        self.resize_windows()

        self.log = Log()
        self.area = Area(60, 40)
        self.player = Actor(self, True)
        self.player.x, self.player.y = 0, self.area.size_y // 2
        self.npcs = []
        for i in range(random.randint(3, 5)):
            self.spawn_npc()

        self.log.add('Welcome to @+%roguelikename%@-, @+@.@-!', colors=(Color.Metal, Color.Skin,))

    def run(self):
        self.update_display()
        self.update_log()
        while True:
            self.log.next_turn()
            while True:
                self.key = self.d.input()
                if not self.d.is_running:
                    return
                if self.key == Key.ResizeDisplay:
                    self.resize_windows()
                    self.update_display()
                    self.update_log()
                else:
                    acted = self.control_player(self.key)
                    self.update_display()
                    self.update_log()
                    if acted:
                        break
            #while not self.player.is_ready():
            self.control_others()
            self.control_environment()
            self.pass_time(self.player.tu if self.player.tu > 0 else self.turn_len)
            self.update_log()

    def update_display(self):
        self.player.calc_vision()
        self.display_map(self.player.x, self.player.y, self.wmap)
        # self.d.prn(self.player.get_sym(), self.wmap.size_x // 2, self.wmap.size_y // 2,
        #            self.player.get_color(), win=self.wmap)

        self.d.fill(' ', win=self.wstat)
        self.d.prn(tactic_abbr[self.player.tactic], 0, 0, tactic_color[self.player.tactic], win=self.wstat)
        self.d.prn('{},{} k={}'.format(self.player.x, self.player.y, self.key),
                   0, 9, win=self.wstat)
        self.d.prn('tu={}'.format(self.player.tu),
                   0, 10, win=self.wstat)

    def disp_to_x(self, dx, ctrx=None, win=None):
        if win is None:
            win = self.wmap
        if ctrx is None:
            ctrx = self.player.x
        return ctrx - win.size_x // 2 + dx

    def disp_to_y(self, dy, ctry=None, win=None):
        if win is None:
            win = self.wmap
        if ctry is None:
            ctry = self.player.y
        return ctry - win.size_y // 2 + dy

    def x_to_disp(self, x, ctrx=None, win=None):
        if win is None:
            win = self.wmap
        if ctrx is None:
            ctrx = self.player.x
        return x - ctrx + win.size_x // 2

    def y_to_disp(self, y, ctry=None, win=None):
        if win is None:
            win = self.wmap
        if ctry is None:
            ctry = self.player.y
        return y - ctry + win.size_y // 2

    def display_map(self, ctrx, ctry, win):
        for r in range(win.size_y):
            my = self.disp_to_y(r, ctry, win)
            self.d.move(win.x, win.y + r, win=win)
            for c in range(win.size_x):
                mx = self.disp_to_x(c, ctrx, win)
                off = my not in range(self.area.size_y) or mx not in range(self.area.size_x)
                if off:
                    self.d.prn(self.offmap_sym, color=self.offmap_color, win=win)
                else:
                    ter = self.area.terrain(mx, my)
                    f1 = int(mx * 3.14) ^ int(my * 1.235)
                    f2 = int(mx * 2.77 + my) ^ int (my + 3.12)
                    colr = ter.get_color(f2) if self.player.is_visible(mx, my) else Color.Dark
                    self.d.prn(ter.get_sym(f1), color=colr, win=win)
        for a in self.npcs + [self.player]:
            self.d.prn(a.get_sym(), self.x_to_disp(a.x, ctrx, win), self.y_to_disp(a.y, ctry, win),
                       a.get_color(), win=win)

    def cell_sym_and_color(self, dx, dy, ctrx=None, ctry=None, win=None):
        x, y = self.disp_to_x(dx, ctrx, win), self.disp_to_y(dy, ctry, win)
        off = y not in range(self.area.size_y) or x not in range(self.area.size_x)
        if off:
            return (self.offmap_sym, self.offmap_color)
        a = self.actor_at(x, y)
        if a is not None:
            return (a.get_sym(), a.get_color())
        ter = reference[self.area.ter[self.area.pos(x, y)]]
        return (ter.get_sym(), ter.get_color())

    def update_log(self):
        self.d.fill(' ', win=self.wlog)
        self.log.prn(self.d, self.wlog)

    def resize_windows(self):
        dsx, dsy = self.d.size()
        self.wstat.size_x = self.inf_x
        self.wstat.size_y = self.inf_y
        self.wmap.size_x = dsx - self.wstat.size_x - 1
        self.wmap.size_y = dsy
        self.wlog.size_x = self.wstat.size_x
        self.wlog.size_y = dsy - self.wstat.size_y - 1
        self.wstat.x = self.wmap.size_x + 1
        self.wlog.x = self.wstat.x
        self.wlog.y = self.wstat.size_y + 1
        for i in range(self.d.stdscr.size_y):
            self.d.prn('│', self.wmap.size_x, i, Color.Metal)
        for i in range(1, self.wstat.size_x):
            self.d.prn('─', i + self.wstat.x - 1, self.wstat.size_y, Color.Metal)
        self.d.prn('├', self.wmap.size_x, self.wstat.size_y, Color.Metal)
        #print ('g/sx{0}/sw{1}/lx{2}/lw{3}/mw{4}'.format(self.wstat.x, self.wstat.size_x, self.wlog.x, self.wlog.size_x, self.wmap.size_x))

    def control_player(self, key):
        tu = self.player.tu
        if key == Key.Up:
            self.player.move(0, -1)
        elif key == Key.Down:
            self.player.move(0, 1)
        elif key == Key.Left:
            self.player.move(-1, 0)
        elif key == Key.Right:
            self.player.move(1, 0)
        elif key == Key.UpLeft:
            self.player.move(-1, -1)
        elif key == Key.UpRight:
            self.player.move(1, -1)
        elif key == Key.DownLeft:
            self.player.move(-1, 1)
        elif key == Key.DownRight:
            self.player.move(1, 1)
        elif key == ord('z'):
            self.player.change_tactic(Tactic.Attack)
        elif key == ord('x'):
            self.player.change_tactic(Tactic.Defence)
        elif key == ord('c'):
            self.player.change_tactic(Tactic.Counter)

        return tu != self.player.tu

    def control_others(self):
        pass

    def control_environment(self):
        pass

    def pass_time(self, tu):
        self.player.pass_time(tu)

    def actor_at(self, x, y):
        if (self.player.x, self.player.y) == (x, y):
            return self.player
        for npc in self.npcs:
            if (npc.x, npc.y) == (x, y):
                return npc
        return None

    def is_occupied(self, x, y):
        if self.area.terrain(x, y).travel <= 0:
            return True
        a = self.actor_at(x, y)
        if a is not None and not a.is_sprawled:
            return True
        return False

    def spawn_npc(self, x=None, y=None):
        while x is None or y is None or self.is_occupied(x, y):
            x = random.randint(5, self.area.size_x - 6)
            y = random.randint(5, self.area.size_y - 6)

        npc = Actor(self)
        npc.x = x
        npc.y = y
        self.npcs.append(npc)
