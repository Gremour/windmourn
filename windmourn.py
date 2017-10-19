#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Main module of the game

from modules.display import Display
from modules.game import Game

ver_major = 0
ver_minor = 0
ver_build = 2

def main():
    d = Display()
    d.set_caption("Windmourn v{}.{}.{}".format(ver_major, ver_minor, ver_build))
    g = Game(d)
    g.run()
    return 0


main()
