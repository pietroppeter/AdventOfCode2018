import re, sys

test_input = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

with open('./inputs/10.txt') as f:
    real_input = f.read()

pattern = re.compile('position=<([\d+\- ]+),([\d+\- ]+)> velocity=<([\d+\- ]+),([\d+\- ]+)>')

# for line in test_input.split('\n'):
#     print(line)
#     match = pattern.match(line)
#     if match is None:
#         print('None')
#     else:
#         print(match.groups())

class Point:

    def __init__(self, x, y, vx, vy, reflect=False):
        self.x = int(x)
        self.y = int(y)
        self.vx = int(vx)
        self.vy = int(vy)
        if reflect:
            self.reflect()
    
    def step(self, n=1):
        self.x += n*self.vx
        self.y += n*self.vy

    def reflect(self):
        self.x, self.y = self.y, self.x
        self.vx, self.vy = self.vy, self.vx

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy})"

def process(text, reflect=False):
    """returns a set of points"""
    points = set()
    for line in text.split('\n'):
        match = pattern.match(line)
        if match is None: continue
        points.add(Point(*match.groups(), reflect=reflect))

    return points

points = process(test_input, reflect=True)
# print(points)

class Grid:

    def __init__(self, max_x=16, max_y=16, min_x=0, min_y=0):
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.reset()
    
    def reset(self):
        # crucial choice: grid as list of rows
        self.grid = [[0 for y in range(self.min_y, self.max_y)] for x in range(self.min_x, self.max_x)]
    
    def add(self, point):
        if self.min_x <= point.x < self.max_x and self.min_y <= point.y < self.max_y:
            self.grid[point.x - self.min_x][point.y - self.min_y] += 1
    
    def count(self):
        return sum([v for row in self.grid for v in row])
    
    def plot(self, meta=True):
        if meta:
            print(grid)
        print('\n'.join([''.join(['#' if v > 0 else '.' for v in row]) for row in self.grid]))
    
    def __repr__(self):
        return f"Grid(max_x={self.max_x}, max_y={self.max_y}, min_x={self.min_x}, min_y={self.min_y}) count: {self.count()}"
        

def bounding(points, border=3):
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for p in points:
        if p.x < min_x:
            min_x = p.x
        elif p.x > max_x:
            max_x = p.x
        if p.y < min_y:
            min_y = p.y
        elif p.y > max_y:
            max_y = p.y
    return max_x + border, max_y + border, min_x - border, min_y - border


grid = Grid(*bounding(points))
grid.plot()

def draw(points, grid, meta=True, seconds=None):
    if seconds is not None:
        print(f"\nSeconds: {seconds}")
    grid.reset()
    for p in points:
        grid.add(p)
    grid.plot(meta=meta)

# plotting test input
draw(points, grid, seconds=0)
for time in range(4):
    for p in points:
        p.step()
    draw(points, grid, seconds=time+1)

# processing real input:
print('\n***Real input')
points = process(real_input)
# 10K steps forward in time
for p in points:
    p.step(n=10_000)
min_size_x = 10_000
min_size_y = 10_000
min_size_t = None
for t in range(1_000):
    for p in points:
        p.step()
    max_x, max_y, min_x, min_y = bounding(points)
    size_x = max_x - min_x
    size_y = max_y - min_y
    if size_x < min_size_x:
        min_size_x = size_x
        min_size_t = t
    if size_y < min_size_y:
        min_size_y = size_y
        min_size_t = t
print(f"min_size_x={min_size_x}, min_size_y={min_size_y}, min_size_t={min_size_t}")
# min_size_x=252, min_size_y=115, min_size_t=239 (run without reflect)

min_size_t = 239
minus_t = -3
plus_t = +3
points = process(real_input, reflect=True)
for p in points:
    p.step(n=10_000 + min_size_t + minus_t)

# redirect print to file
with open('./python/day10out.txt', 'w') as f:
    sys.stdout = f

    for t in range(plus_t - minus_t):
        for p in points:
            p.step()
        grid = Grid(*bounding(points))
        draw(points, grid, seconds=10_000 + min_size_t + minus_t + t + 1)