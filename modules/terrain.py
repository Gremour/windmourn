# -*- coding: utf-8 -*-

from modules.display import Color
import random


class Terrain:
    """Class, describing constant properties of one square of local map."""
    def __init__(self, name, sym, color, cover=0.0,
                       vision=1.0, travel=1.0):
        self.name = name
        self.sym = sym
        self.color = color
        self.cover = cover
        self.vision = vision
        self.travel = travel

    def get_color(self, feature=-1):
        is_list = type(self.color) == list
        if feature < 0:
            feature = random.getrandbits(32)
        lenff = 1 if not is_list else len(self.color)
        if is_list:
            return self.color[feature % lenff]
        else:
            return self.color

    def get_sym(self, feature=-1):
        if feature < 0:
            feature = random.getrandbits(32)
        lenff = 1 if len(self.sym) < 1 else len(self.sym)
        if len(self.sym) < 2:
            return self.sym
        else:
            return self.sym[feature % lenff]

# No duplicate names allowed!
reference = [
    Terrain('under construction', '?', Color.Weird),
    Terrain('grass', '.,', [Color.Green, Color.Pine, Color.Yellow],
        travel=0.95),
    Terrain('gravel', ':', Color.DarkYellow, travel=0.8),
    Terrain('red', '*', Color.Red, travel=0.8),
    Terrain('blue', '*', Color.Blue, travel=0.8),
    Terrain('yellow', '*', Color.Yellow, travel=0.8),
    Terrain('floor', '.', Color.Concrete),
    Terrain('pine', 'T', Color.Pine, travel=0, vision=0.5, cover=0.6),
    Terrain('tree stump', 'n', Color.Brown, travel=0.3, vision=0.9, cover=0.4),
    Terrain('rubble', '&', [Color.Concrete, Color.Dark], travel=0.3),
    Terrain('brick rubble', '&', [Color.DarkRed, Color.Red], travel=0.25),
    Terrain('metal rubble', '&', [Color.Cyan, Color.Metal], travel=0.2),
    Terrain('brick wall', '#', Color.DarkRed, travel=0, vision=0, cover=1),
    Terrain('metal wall', '#', Color.Metal, travel=0, vision=0, cover=1),
    Terrain('closed door', '+', Color.Brown, travel=0, vision=0, cover=1),
    Terrain('open door', '/', Color.Brown, travel=0.9, vision=0.9, cover=0.2)
    ]

ter_names = [ter.name for ter in reference]
assert len(ter_names) == len(set(ter_names)), \
    "terrain.reference contains duplicate names"


name2num = {name: i for i, name in enumerate(ter_names)}
