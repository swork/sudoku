import color
import sys, re

def print_grid(p0, p_from, indent=0):
    r = color.reset()
    for y in range(0,9):
        sys.stdout.write(" " * indent)
        sys.stdout.write("|")
        for x in range(0,9):
            v = p0[y][x]
            c = color.select(y, x, p0, p_from)
            r = color.reset() if c else ""
            sys.stdout.write(" %s%s%s " % (c, str(v) if v else " ", r))
        sys.stdout.write("|\n")
    sys.stdout.write("\n")

pipe_line = re.compile(r"^ (\s*) \| ((\s|\d)+) ([|])? (\s+)? $", re.X)
nopipe_line = re.compile(r"^ () ((\s|\d)+?)$", re.X)

def read_puzzle(f):
    """
    Accept nine rows of puzzle as lines (empty don't count) of "sp digit sp" or
    "sp sp sp" starting with first vertical-bar (start of line if none). Fill
    with zeroes if line is short.
    """
    p = list()
    skipped = 0
    for yi, line in enumerate(f):
        yi -= skipped
        line = line.rstrip()
        row = list()
        #print(yi, repr(line))
        if len(line) == 0:
            skipped += 1
            continue
        mo =  pipe_line.match(line)
        if mo is None:
            mo = nopipe_line.match(line)
        input_ascii = bytearray(mo.groups()[1], "ascii", "ignore")
        #print(input_ascii)
        for xi in range(0,9):
            if len(input_ascii):
                assert(input_ascii.pop(0) == ord(' '))
            if len(input_ascii):
                ch = input_ascii.pop(0)
                if ch >= ord('0') and ch <= ord('9'):
                    row.append(ch - ord('0'))
                elif ch == ord(' '):
                    row.append(0)
            else:
                row.append(0)
            #print(xi, row[-1])
            if len(input_ascii):
                if input_ascii[0] == ord('|'):
                    input_ascii = bytes()
            if len(input_ascii):
                assert(input_ascii.pop(0) == ord(' '))
        p.append(row)
        if yi >= 8:
            break
    return p
