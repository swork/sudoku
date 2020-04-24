#! /usr/bin/env python3

import sys, re
from copy import deepcopy
from functools import total_ordering
from .util import print_grid

class DeadEnd(Exception):
    pass

OneThruNine = set(range(1,9+1))
Colorize = False
Debug = 0

def debug(d=1):
    global Debug
    Debug = d

@total_ordering
class Cell:
    def __init__(self, p, y, x, v=0):
        self.p = p
        self.y = y
        self.x = x
        self.v = v

    def __repr__(self):
        return "<Cell y:%d x:%d v:%d>" % (self.y, self.x, self.v)

    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def getKey(self):
        return (self.y, self.x)

    def possible(self):
        if self.v:
            return set([self.v])
        claimed = set()
        claimed.update(self.p.rowvals(self.y))
        claimed.update(self.p.colvals(self.x))
        claimed.update(self.p.sqrvals(self.y, self.x))
        poss = OneThruNine - claimed
        if Debug > 0:
            print("%d,%d: %s" % (self.y, self.x, poss))
        if len(poss) == 0:
            raise DeadEnd
        return poss

    def preflight(self):
        if self.v == 0:
            return None
        if self.p.rowvals(self.y).count(self.v) > 1:
            return False
        if self.p.colvals(self.x).count(self.v) > 1:
            return False
        if self.p.sqrvals(self.y, self.x).count(self.v) > 1:
            return False
        return None


class Puzzle:
    def __init__(self, p):
        """
        Make a Sudoku puzzle from a grid (tuple of tuples) of values
        with zeroes representing unknowns
        """
        self.cells = list()
        for y, row in enumerate(p):
            self.cells.append(list())
            for x, v in enumerate(row):
                self.cells[y].append(Cell(self, y, x, v))

    def expand(self):
        """
        Given a Puzzle instance, return a grid of all possibilities.
        """
        rows = list()
        self.unresolved = set()
        for y in range(0,9):
            rows.append(list())
            for x in range(0,9):
                p = sorted(self.possible(y,x))
                if len(p) == 0:
                    raise DeadEnd()
                rows[y].append(p)
                if len(p) != 1:
                    self.unresolved.add(self.cells[y][x])
        return rows

    def _elim_from_others_poss(self, v, y, x):
        if Debug:
            print("_elim %d,%d: %d" % (y, x, v))
        for i in range(0,9):
            yi = (y // 3) * 3 + i // 3
            xi = (x // 3) * 3 + i % 3
            if Debug:
                print("  %d,%d:%s" % (y, i, self.cells[y][i]._poss))
                print("  %d,%d:%s" % (i, x, self.cells[i][x]._poss))
                print("  %d,%d:%s" % (yi, xi, self.cells[yi][xi]._poss))
            if i != x:
                try: self.cells[y][i]._poss.remove(v)
                except (KeyError, AttributeError): pass
            if i != y:
                try: self.cells[i][x]._poss.remove(v)
                except (KeyError, AttributeError): pass
            if yi != y and xi != x:
                try: self.cells[yi][xi]._poss.remove(v)
                except (KeyError, AttributeError): pass

    def resolve(self):
        """
        Given a Puzzle instance, return a grid with all one-option locations
        filled in and zeroes for all unknown locations.
        """
        rows = list()
        self.unresolved = set()
        for y in range(0,9):
            rows.append(list())
            for x in range(0,9):
                if not self.cells[y][x].v:
                    p = self.possible(y,x)
                    if len(p) == 0:
                        raise DeadEnd
                    self.cells[y][x]._poss = p
                    self.unresolved.add(self.cells[y][x])
                else:
                    # Avoid some awkward tests in debug cases
                    self.cells[y][x]._poss = set([self.cells[y][x].v])

        # Repeatedly check for only-poss values and eliminate them from neighbs
        last_grid = None
        while True:
            resolved = set()
            done1 = False

            if Debug:
                grid = self.get_grid()
                print_grid(grid, last_grid)
                last_grid = grid

            for c in self.unresolved:
                if len(c._poss) == 1:
                    if Debug:
                        print("%s has 1 _poss: %s" % (c, c._poss))
                    done1 = True
                    c.v = list(c._poss)[0]  # ref so self.cells.v too
                    self._elim_from_others_poss(c.v, c.y, c.x)
                    resolved.add(c)
            self.unresolved -= resolved
            if not done1:
                break
        return self.get_grid()

    def get_grid(self):
        rows = list()
        for yi in range(0,9):
            rows.append(list())
            for xi in range(0,9):
                rows[yi].append(self.cells[yi][xi].v)
        return rows

    def rowvals(self, y):
        s = list()
        for xi in range(0, 9):
            v = self.cells[y][xi].v
            if v:
                s.append(v)
        if Debug > 1:
            print("rowvals %d: %s" % (y,repr(sorted(s))))
        return s

    def colvals(self, x):
        s = list()
        for yi in range(0, 9):
            v = self.cells[yi][x].v
            if v:
                s.append(v)
        if Debug > 1:
            print("colvals %d: %s" % (x,repr(sorted(s))))
        return s

    def sqrvals(self, y, x):
        s = list()
        ys = (y // 3) * 3
        xs = (x // 3) * 3
        for yi in range(ys, ys+3):
            for xi in range(xs, xs+3):
                v = self.cells[yi][xi].v
                if v:
                    s.append(v)
        if Debug > 1:
            print("sqr %d,%d: %s" % (y,x,repr(sorted(s))))
        return s

    def possible(self, y, x):
        return self.cells[y][x].possible()

    def preflight(self):
        any_v = False
        for y in range(0,9):
            for x in range(0,9):
                if self.cells[y][x].preflight() == False:
                    return False  # illegal input
                if not any_v and self.cells[y][x].v != 0:
                    any_v = True
        if not any_v:
            return True  # unconstrained input
        return None

    def split(self):
        variants = list()
        split_on = list(self.unresolved)[0]  # pick one
        for v in split_on.possible():
            rows = list()
            for y in range(0,9):
                rows.append(list())
                for x in range(0,9):
                    if y == split_on.y and x == split_on.x:
                        rows[y].append(v)
                    else:
                        rows[y].append(self.cells[y][x].v)
            variants.append(rows)
        return sorted(variants)
