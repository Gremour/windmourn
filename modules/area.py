# -*- coding: utf-8 -*-

from modules.terrain import reference, name2num

from array import array
import random


class Area:
    """Local map, consisting of terrain array, and objects, and NPCs"""
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.diameter = int((self.size_x * self.size_y) ** 0.5)
        self.ter = array('h', (0,) * size_x * size_y)
        self.gen_plains()

    def terrain(self, x, y):
        return reference[self.ter[self.pos(x, y)]]

    def change_terrain(self, x, y, tername):
        self.ter[self.pos(x, y)] = name2num[tername]

    def pos(self, x, y):
        pos = x + y * self.size_x
        assert pos in range(self.size_x * self.size_y), \
            'Area.pos invalid values {0},{1} out of {2},{3}'.format(
                x, y, self.size_x, self.size_y)
        return pos

    def rand_pos(self, border=0):
        return (random.randint(border, self.size_x - 1 - border),
                random.randint(border, self.size_y - 1 - border))

    def gen_plains(self):
        self.fill_rect(0, 0, self.size_x, self.size_y,
            ['grass'])
        self.fill_rect(0, 0, self.size_x, self.size_y,
            ['pine', 'tree stump'], 0.05)

        num_gravel = self.diameter // 5
        for i in range(num_gravel):
            rr = random.randint(4, 8)
            rx, ry = self.rand_pos(rr)
            self.fill_ellipse(rx - rr, ry - rr, rr * 2, rr * 2,
                ['gravel'], 0.7)

        num_rubble = self.diameter // 10 + 1
        for i in range(num_rubble):
            rr = random.randint(2, 5)
            rx, ry = self.rand_pos(rr)
            self.fill_ellipse(rx - rr, ry - rr, rr * 2, rr * 2,
                ['rubble'], 0.3)

        num_buildings = random.randint(1, 2 + self.diameter // 20)
        for i in range(num_buildings):
            bw = random.randint(5, 10)
            bh = random.randint(5, 10)
            bx, by = self.rand_pos(max(bw, bh) + 2)
            bx -= bw // 2
            by -= bh // 2
            ruin = True if random.randrange(5) > 0 else False
            metal = True if random.randrange(10) == 0 else False
            self.gen_building(bx, by, bw, bh, ruin, metal)

    def gen_building(self, x, y, w, h, ruin=False, metal=False):
        wall = ['metal wall'] if metal else ['brick wall']
        self.fill_rect(x + 1, y + 1, w - 2, h - 2, ['floor'])
        self.draw_rect(x, y, w, h, wall)
        side = random.randrange(4)
        dr = random.randint(1, (w if side % 2 else h) - 2)
        doorx = (x + dr) if side % 2 else (x if side == 0 else x + w - 1)
        doory = (y + dr) if not side % 2 else (y if side == 1 else y + h - 1)
        door = random.choice(['open door', 'closed door'])
        self.ter[self.pos(doorx, doory)] = name2num[door]
        if (ruin):
            rubble = ['metal rubble'] if metal else ['brick rubble']
            self.draw_rect(x, y, w, h, rubble, 0.3)
            self.draw_rect(x, y, w, h, ['floor'], 0.1)
            self.fill_rect(x + 1, y + 1, w - 2, h - 2, ['grass'], 0.3)
            self.fill_rect(x + 1, y + 1, w - 2, h - 2, rubble, 0.2)
            self.ter[self.pos(doorx, doory)] = name2num[door]

    def draw_rect(self, x, y, w, h, terlist, density=1.0):
            self.fill_rect(x, y, w, 1, terlist, density)
            self.fill_rect(x, y + h - 1, w, 1, terlist, density)
            self.fill_rect(x, y, 1, h, terlist, density)
            self.fill_rect(x + w - 1, y, 1, h, terlist, density)

    def fill_rect(self, x, y, w, h, terlist, density=1.0):
        #print("fill_rect {0},{1} {2}x{3}".format(x, y, w, h))
        for r in range(y, y + h):
            for c in range(x, x + w):
                if density >= 1 or random.random() < density:
                    self.ter[self.pos(c, r)] = name2num[
                        random.choice(terlist)]

    def fill_ellipse(self, x, y, w, h, terlist, density=1.0):
        xc = x + w / 2
        yc = y + h / 2
        mr = w * h
        for r in range(y, y + h):
            for c in range(x, x + w):
                if (c - xc) ** 2 + ((r - yc) * h / w) ** 2 > mr:
                    continue
                if density >= 1 or random.random() < density:
                    self.ter[self.pos(c, r)] = name2num[
                        random.choice(terlist)]

