test_input = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

with open('./inputs/06.txt') as f:
    my_input = f.read()

# to solve this I will use two bizarre objects: Pointy and Mappy
# this is not particularly good OOP
class Pointy:

    def __init__(self, x, y, i=None, d=0):
        self.x = x
        self.y = y
        self.i = i  # to which point is assigned: None not assigned, -1: conflicted
        self.d = d  # distance to point which is assigned
    
    def border(self, d, mappy):
        coords = {(self.x + x_abs*signs[0], self.y + (d - x_abs)*signs[1])
                  for x_abs in range(d + 1)
                  for signs in [(1,1), (1, -1), (-1, -1), (-1, 1)]}
        return [Pointy(c[0], c[1], self.i, d) for c in coords if 0 <= c[0] <= mappy.max_x and 0 <= c[1] <= mappy.max_y]

    def __repr__(self):
        return f"Pointy(x={self.x}, y={self.y}, i={self.i}, d={self.d})"
    
    def __str__(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        if self.i == -1:
            return '.'
        elif self.i is None:
            return ' '
        elif self.d == 0:
            return alphabet[self.i % len(alphabet)].upper()
        else:
            return alphabet[self.i % len(alphabet)]

class Mappy:

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.grid = [[Pointy(x, y) for y in range(self.max_y + 1)] for x in range(self.max_x + 1)]
        self.points = list()
    
    def assign(self, point):
        if self.grid[point.x][point.y].i is None:
            self.grid[point.x][point.y] = point
            if point.d == 0:
                self.points.append(point)
            return 1
        elif self.grid[point.x][point.y].d == point.d:
            self.grid[point.x][point.y].i = -1  # mark conflict
        return 0

    def extend(self, d):
        filt = list()
        tot_count = 0
        for j, p in enumerate(self.points):
            count = 0
            for q in p.border(d, self):
                count += self.assign(q)
            if count == 0:
                filt.append(j)
            tot_count += count
        # remove points that did not extend
        self.points = [p for j, p in enumerate(self.points) if j not in filt]
        return tot_count

    def plot(self):
        print('\n'.join([''.join([str(v) for v in row]) for row in self.grid]))
    
    def max_area(self):
        areas = dict()
        border_indexes = set()
        for row in self.grid:
            for p in row:
                if p.i >= 0:
                    if  p.i in areas:
                        areas[p.i] += 1
                    else:
                        areas[p.i] = 1
                    if p.x == 0 or p.y == 0 or p.x == self.max_x or p.y == self.max_y:
                        border_indexes.add(p.i)
        return max([v for k, v in areas.items() if k not in border_indexes])#, areas, border_indexes

# global and modified by process
max_x = 0
max_y = 0

def line_to_coords(line):
    seq = line.split(',')
    x = int(seq[0])
    y = int(seq[1])
    return x, y

def process(text):
    global max_x, max_y
    points = list()
    for i, line in enumerate(text.split('\n')):
        y, x = line_to_coords(line)
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        points.append(Pointy(x, y, i=i))
    mappy = Mappy(max_x, max_y)
    for p in points:
        mappy.assign(p)
    return points, mappy

points, mappy = process(test_input)
print("#points: ", len(points))
print(f"max_x={max_x}, max_y={max_y}")

# print(points[0])
# border = points[0].border(1, mappy)
# print(len(border), border)
# border = points[0].border(2, mappy)
# print(len(border), border)
# border = points[0].border(3, mappy)
# print(len(border))
# border = points[3].border(2, mappy)
# print(len(border))
# border = points[3].border(3, mappy)
# print(len(border))

print("extending pins on mappy")
for d in range(1, 10):
    # print(d)
    tot_count = mappy.extend(d)
    # print(tot_count)
    if tot_count == 0:
        break
mappy.plot()
# from Advent of Code:
# aaaaa.cccc
# aAaaa.cccc
# aaaddecccc
# aadddeccCc
# ..dDdeeccc
# bb.deEeecc
# bBb.eeee..
# bbb.eeefff
# bbb.eeffff
# bbb.ffffFf

# My plot:
# aaaaa.ccc
# aAaaa.ccc
# aaaddeccc
# aadddeccC
# ..dDdeecc
# bb.deEeec
# bBb.eeee.
# bbb.eeeff
# bbb.eefff
# bbb.ffffF
print(mappy.max_area())

# my input
print("my input")
points, mappy = process(my_input)
print("#points: ", len(points))
print(f"max_x={max_x}, max_y={max_y}")

print("extending pins on mappy")
for d in range(1, 200):
    # print(d)
    tot_count = mappy.extend(d)
    # print(tot_count)
    if tot_count == 0:
        break
print(tot_count)
print(mappy.max_area())
