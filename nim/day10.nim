import re, strutils, strformat, sets, hashes, math, sequtils

# pattern cannot be a const! why?
const test_input = """position=< 9,  1> velocity=< 0,  2>
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

const my_input = readFile("./inputs/10.txt")

type
  Point = ref object
    x, y, vx, vy: int
  PointSet = HashSet[Point]

var 
  point: Point
  pointSet: PointSet

proc `$`(p: Point): string =
  fmt"Point(x={p.x}, y={p.y}, vx={p.vx}, vy={p.vy})"

proc hash(p: Point): Hash =
  ## Computes a Hash from point `p`.
  var h: Hash = 0
  h = h !& hash(p.x)
  h = h !& hash(p.y)
  h = h !& hash(p.vx)
  h = h !& hash(p.vy)
  result = !$h

proc process(input: string): PointSet =
  let
    lines = toSeq(input.splitLines())
    initialsize = nextPowerOfTwo(lines.len)
    pattern = re"position=<([\d+\- ]+),([\d+\- ]+)> velocity=<([\d+\- ]+),([\d+\- ]+)>"
  var
    matches: array[4, string]
    point: Point
  result = initSet[Point](initialsize)
  for line in lines:
    # echo line
    if match(line, pattern, matches):
      # echo matches
      # transposing
      point = Point(y: parseInt(matches[0].strip()), x: parseInt(matches[1].strip()),
                    vy: parseInt(matches[2].strip()), vx: parseInt(matches[3].strip()))
      # echo point
      result.incl(point)

echo "processing test input"
pointSet = process(test_input)
echo "#Points ", card(pointSet)

type
  Grid = ref object
    maxX, maxY, minX, minY: int
    data: seq[seq[int]]  # I would like to make something more efficient with arrays
var
  grid: Grid

proc reset(grid: var Grid) =
  var
    row: seq[int]
  grid.data = @[]
  for x in grid.minX .. grid.maxX:
    row = @[]
    for y in grid.minY .. grid.maxY:
      row.add(0)
    grid.data.add(row)

proc initGrid(pointSet: PointSet): Grid =
  var
    maxX, maxY, minX, minY: int

  # getting min and max to initialize grid
  for p in pointSet:
    # here I copy and paste from Python and I do not have to correct (thanks to Nim id insensitivity)
    if p.x < min_x:
        min_x = p.x
    elif p.x > max_x:
        max_x = p.x
    if p.y < min_y:
        min_y = p.y
    elif p.y > max_y:
        max_y = p.y
  result = Grid(maxX: maxX, maxY: maxY, minX: minX, minY: minY, data: @[])
  result.reset()

  # fill grid with points
  for p in pointSet:
    result.data[p.x - result.minX][p.y - result.minY] += 1

proc plot(grid: Grid): string =
  var lines: seq[string]
  for row in grid.data:
    lines.add row.mapIt(if it > 0: "#" else: ".").join()
  lines.join(sep="\n")

# plotting test input
grid = initGrid(pointSet)
echo "Initial Grid"
echo grid.plot

proc step(p: Point, n: int = 1): Point =
  # I would like to have it as a non returning method:
  # point.x += n*point.vx
  # point.y += n*point.vy
  # but for next step on pointSet I need it like this
  Point(x: p.x + n*p.vx, y: p.y + n*p.vy, vx: p.vx, vy: p.vy)

# I would like to modify inplace the pointSet but I was not able to
proc step(pointSet: var PointSet, n: int = 1): PointSet =
  var
    point: Point
  result = initSet[Point](pointSet.len.nextPowerOfTwo)
  for p in pointSet:
    point = p.step(n)
    result.incl(point)

for time in 1..4:
  echo "\nSeconds: ", time
  pointSet = pointSet.step()
  echo initGrid(pointSet).plot

echo "My input"
pointSet = process(myInput)
echo "#Points ", card(pointSet)

let waitTime = 10_000 + 239 + 1
pointSet = pointSet.step(waitTime)

writeFile("./nim/day10out.txt", pointSet.initGrid.plot)
echo "Wait time: ", waitTime