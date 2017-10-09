# -*- coding: utf-8 -*-

from modules.display import Color
from modules.log import vowels
from modules.algos import bresenham
from enum import IntEnum
import random
from array import array

class Tactic(IntEnum):
    Attack = 0
    Defence = 1
    Counter = 2


tactic_name = [ 'attack', 'defence', 'counterattack' ]
tactic_abbr = [ 'atk', 'def', 'ctr' ]
tactic_color = [ Color.Red, Color.Blue, Color.Yellow ]


class Actor:
    """Player or non-player character"""

    vision_unknown = 255

    def __init__(self, game, player=False):
        self.g = game
        self.is_player = player
        self.x = 0
        self.y = 0
        self.tu = 0
        self.tactic = Tactic.Attack
        self.unc = False
        self.hp = 3
        self.is_sprawled = False
        self.vision = 0.6   # How inobstructive vision through this actor is 0..1
        self.eyes = 1       # How good is actor's vision 0..1
        if self.is_player:
            self.vision_dim = game.vision_range * 2 + 1
            self.vision_arr = array('B', (self.vision_unknown,) * self.vision_dim * self.vision_dim)

    def calc_vision(self):
        """Calculate vision array for this actor"""
        assert self.is_player, "vision array is only defined for player!"

        def gen_border(a):
            for ind in range(a.vision_dim):
                yield (ind, 0)
                yield (ind, a.vision_dim-1)
                if ind in range(1, a.vision_dim-1):
                    yield (0, ind)
                    yield (a.vision_dim-1, ind)

        for i in range(self.vision_dim * self.vision_dim):
            self.vision_arr[i] = self.vision_unknown

        kdark = 1.0 / self.g.vision_range
        for (vx, vy) in gen_border(self):
            # vx, vy = is inside self.vision_arr, i.e. in range(self.vision_dim), iterating over border of vision_arr
            # rx, ry = is relative of player position, i.e. in range(-self.vision_dim//2, self.vision_dim//2+1)
            # cx, cy = is current calculated cell, same range as rx, ry
            # tx, ty = is coordinates inside area
            vision = int(self.eyes * 250)
            d = self.vision_dim // 2
            rx = vx - d
            ry = vy - d
            r = 0
            for (cx, cy) in bresenham((0, 0), (rx, ry)):
                if r >= self.g.vision_range:
                    break
                tx = self.x + cx
                ty = self.y + cy
                if tx not in range(self.g.area.size_x) or \
                   ty not in range(self.g.area.size_y):
                    self.vision_arr[cx + d + (cy + d) * self.vision_dim] = 0
                    break
                cv = self.vision_arr[cx + d + (cy + d) * self.vision_dim]
                if cv != self.vision_unknown:
                    vision = cv
                    continue
                if vision:
                    tv = self.g.area.terrain(tx, ty).vision
                    vision = int(vision * tv * kdark)
                self.vision_arr[cx + d + (cy + d) * self.vision_dim] = vision
                r += 1

        # for y in range(self.vision_dim):
        #     s = ""
        #     for x in range(self.vision_dim):
        #         s += "{0:2x}".format(self.vision_arr[x + y * self.vision_dim])
        #     print (s)


    def is_visible(self, x, y):
        vx = x - self.x
        vy = y - self.y
        visible = vx in range(-self.g.vision_range, self.g.vision_range * 2 + 1) and \
                  vy in range(-self.g.vision_range, self.g.vision_range * 2 + 1) and \
                  self.vision_arr[vx + vy * self.vision_dim] > 0

    def pass_time(self, tu):
        self.tu -= tu

    def is_ready(self):
        return self.tu <= 0

    def get_sym(self):
        return '@'

    def get_color(self):
        if self.g.player == self:
            return Color.Skin
        return Color.Dark

    def get_name(self):
        if self.g.player == self:
            return 'you'
        return 'assassin'

    def s(self):
        return '' if self.is_player else 's'

    def target(self, dx, dy):
        tx, ty = self.x + dx, self.y + dy
        if tx not in range(self.g.area.size_x) \
            or ty not in range(self.g.area.size_y):
            return None
        a = self.g.actor_at(tx, ty)
        if a is not None and not a.is_sprawled:
            return a
        return self.g.area.terrain(tx, ty)

    def move(self, dx, dy):
        if self.is_sprawled:
            self.stand_up()
            return
        if dx == 0 and dy == 0:
            #wait
            self.tu += self.g.turn_len
            return
        tar = self.target(dx, dy)
        if tar is None:
            return
        elif type(tar) is Actor:
            self.attack(tar)
        else:
            trv = tar.travel
            if tar.name == 'closed door':
                self.open_door(dx, dy)
                return
            an = 'n' if tar.name[0] in vowels else ''
            if trv <= 0:
                if self.is_player:
                    self.g.log.add("you stumble upon a{n} {ter}".format(n=an, ter=tar.name))
                self.tu += self.g.turn_len
                return
            elif trv < 0.8:
                if random.randrange(100) < (1 - tar.travel) * 50:
                    self.g.log.add("{me} trip{s} and fall{s} down".format(me=self.get_name(), s=self.s()))
                    self.is_sprawled = True
                else:
                    if self.is_player:
                        self.g.log.add("you pass a{n} {ter}, which slows you down.".format(n=an, ter=tar.name))
            self.x, self.y = self.x + dx, self.y + dy
            self.tu += int(self.g.turn_len / tar.travel)

    def stand_up(self):
        if self.g.is_occupied(self.x, self.y):
            if self.is_player:
                self.g.log.add("You cant's stand up, something blocks your way")
            return

        self.tu += 200
        self.is_sprawled = False
        self.g.log.add("{me} stand{s} up".format(me=self.get_name(), s=self.s()))

    def open_door(self, dx, dy):
        ter = self.target(dx, dy)
        if ter.name == 'closed door':
            self.g.area.change_terrain(self.x + dx, self.y + dy, 'open door')
            self.tu += self.g.turn_len
            self.g.log.add("{me} open{s} the door".format(me=self.get_name(), s=self.s()))

    def attack(self, a):
        self.tu += self.g.turn_len
        self.g.log.add("{me} @+attack{s}@- {tar}".format(me=self.get_name(), s=self.s(), tar=a.get_name()), (tactic_color[self.tactic],))
        a.wound()

    def change_tactic(self, tac):
        if tac == self.tactic:
            return
        self.tu += 60
        self.tactic = tac
        self.g.log.add("{me} change{s} tactics to @+{tac}@-".format(me=self.get_name(), s=self.s(), tac=tactic_name[self.tactic]),
                       (tactic_color[self.tactic],))

    def wound(self):
        con = self.is_conscious()
        if self.hp > 0:
            self.hp -= 1
        self.unc = self.hp <= 0
        if not self.is_conscious() and con:
            self.is_sprawled = True
            self.g.log.add("{me} fall{s} down unconscious".format(me=self.get_name(), s=self.s()))

    def is_conscious(self):
        return not self.unc;