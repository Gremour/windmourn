#!/usr/bin/python3
# -*- coding: utf-8 -*-

from modules.display import Display
from modules.game import Game


def main():
    d = Display()
    g = Game(d)
    g.run()
    return 0


main()
