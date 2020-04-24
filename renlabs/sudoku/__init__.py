from . import puzzle, color
import re, argparse, sys, logging, json
from copy import deepcopy
from .puzzle import Puzzle, DeadEnd
from .util import print_grid, read_puzzle

logger = logging.getLogger(__name__ if not __name__ == '__main__' else os.path.basename(__file__))

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

class Sudoku:
    def __init__(self):
        self._input = None
        self._solution = None
        self._resolved = False

    def inputList(self, input):
        self._resolved = False
        self._solution = None
        if len(input) > 9:
            raise ValueError('Too many rows in input')
        for row in input:
            while len(row) < 9:
                row.append(0)
            if len(row) > 9:
                raise ValueError(f'Too many columns in input row {row!r}')
        while len(input) < 9:
            input.append([0,] * 9)
        self._input = input

    def inputJson(self, jstr):
        l = json.loads(jstr)
        self.inputList(l)

    def preflight(self):
        puz = Puzzle(self._input)
        return puz.preflight()

    @property
    def solution(self):
        if not self._resolved:
            self._resolved = True
            self._solution = solve_c(self._input, self._input)
        return self._solution

    def print_solved_simple(self):
        if self.solution:
            print_grid(self.solution, self._input)
        else:
            print("No solution.")

    def print_solved_json(self):
        if self.solution:
            print(json.dumps(self.solution, separators=(',',':')))  # lose spaces
        else:
            print(json.dumps([]))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--debug', action='store_true')
    p.add_argument('--json', '-j')
    p.add_argument('--predefined', action='store_true')
    a = p.parse_args()

    if a.debug:
        logger.setLevel(logging.DEBUG)

    s = Sudoku()

    if a.predefined:
        s.inputList([
            [ 0, 0, 9, 0, 7, 0, 0, 8, 4 ],
            [ 0, 7, 6, 8, 0, 9 ],
            [ 0, 0, 0, 0, 0, 3, 0, 0, 2 ],
            [ 0, 1, 0, 0, 3 ],
            [ 0, 2, 0, 4 ],
            [ 0, 0, 0, 9, 2, 0, 0, 6 ],
            [ 0, 0, 7, 6, 5, 4, 0, 3 ],
            [ 0, 5, 0, 0, 0, 1 ],
            [ 0, 0, 0, 0, 0, 2, 0, 9 ]
        ])
    elif a.json:
        if a.json[0] == '@':
            with open(a.json[1:]) as f:
                s.inputList(json.load(f))
        else:
            s.inputList(json.loads(a.json))
    else:
        print("Need input. '--json='?")
        return 99

    if a.json:
        s.print_solved_json()
    else:
        s.print_solved_simple()
    return 0
