#! /usr/bin/env python3

import sys

RESET = "\x1b[0m"
RED = "\x1b[41;37;1m"
BLUE = "\x1b[44;1m"
GREEN = "\x1b[42;1m"

Colorize = True
Out = sys.stdout

def init(colorize=False, outstream=sys.stdout):
    global Colorize
    Colorize = colorize
    Out = outstream

def reset():
    if Colorize:
        return RESET
    return ""

def select(y, x, p, po=None, c=RED):
    """
    p is a sudoku.py grid, a 9x9 array of numbers 1-9.
    If po, it's a grid like p.
    If coord's values differ p/po, return c.
    """
    if Colorize and po:
        if p[y][x] != po[y][x]:
            return c
    return ""
