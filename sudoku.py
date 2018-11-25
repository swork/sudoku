#! /usr/bin/env python3

import puzzle, color
import re, argparse, sys
from copy import deepcopy
from puzzle import Puzzle, DeadEnd
from util import print_grid, read_puzzle

def solve_c(p0, p_from, recursion_depth=0):
    indent = " " * recursion_depth
    puz = Puzzle(p0)
    p1 = puz.resolve()
    if len(puz.unresolved) == 0:
        return p1
    if puzzle.Debug:
        print("%s%d: u%d" % (indent, recursion_depth, len(puz.unresolved)))
        print_grid(p1, p_from, recursion_depth)
    unr = sorted(puz.unresolved)
    for i in range(2,9):
        for c in unr:
            poss = c.possible()
            if len(poss) != i:
                continue
            if puzzle.Debug:
                print("%s%d: %s %s" % (indent, recursion_depth, c, poss))
            for v in sorted(poss):
                if puzzle.Debug:
                    print("%d <== for (%d,%d).v:%d" % (recursion_depth+1, c.y, c.x, v))
                p2 = deepcopy(p1)
                p2[c.y][c.x] = v
                try:
                    return solve_c(p2, p1, recursion_depth + 1)
                except DeadEnd:
                    if puzzle.Debug:
                        print("%d DeadEnd (%d,%d).v:%d" % (recursion_depth+1, c.y, c.x, v))
            raise DeadEnd


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--predefined", "-p", action="store_true")
    parser.add_argument("--color", "-c", action="store_true")
    parser.add_argument("--debug", "-d", action="store_true")
    a = parser.parse_args()
    if a.color:
        color.init(True)
    else:
        color.init(False)
    if a.predefined:
        p0 = read_puzzle("""
            |       9     7        8  4 |
            |    7  6  8     9          |
            |                3        2 |
            |    1        3             |
            |    2     4                |
            |          9  2        6    |
            |       7  6  5  4     3    |
            |    5           1          |
            |                2     9    |
            """.split('\n'))
    else:
        p0 = read_puzzle(sys.stdin)

    if a.debug:
        puzzle.debug(2)

    print_grid(p0, p0)
    p = solve_c(p0, p0)
    if p:
        print_grid(p, p0)
    else:
        print("No solution.")
