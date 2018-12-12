import strutils, times, memo

proc hundredDigit(n: int): int =
  let ns = $n
  if ns.len > 2:
    return parseInt($ns[^3])
  return 0

echo 12.hundredDigit
echo 123.hundredDigit
echo 43210.hundredDigit
echo 4321.hundredDigit

proc powerLevel(x, y, serial: int): int {.memoized.} =
  let rackId = x + 10
  hundredDigit((rackId*y + serial)*rackId) - 5

echo powerLevel(3, 5, 8)
echo(power_level(122, 79, 57), "== -5")
echo(power_level(217, 196, 39), "== 0")
echo(power_level(101, 153, 71), "== 4")

# non memo version
proc squareTotalPower(x, y, serial, size: int): int =
  for i in 0 ..< size:
    for j in 0 ..< size:
      result += powerLevel(x + i, y + j, serial)

proc squareTotalPowerMemo(x, y, serial, size: int): int {.memoized.} =
  if size <= 3:
    return squareTotalPower(x, y, serial, size)
  result += squareTotalPowerMemo(x, y, serial, size - 1)
  for i in 0 ..< size: # side plus corner
    result += powerLevel(x + i, y + size - 1, serial)
  for j in 0 ..< size - 1:  # only side
    result += powerLevel(x + size - 1, y + j, serial)

echo squareTotalPower(33, 45, 18, 3)
echo squareTotalPower(21, 61, 42, 3)

proc solve(serial, sizeLow, sizeHigh: int) =
  const sizeGrid = 300
  var
    power: int
    maxPower = -100
    xs = -1
    ys = -1
    sizeBest = -1
    coordHigh: int
  for sizeSquare in sizeLow .. sizeHigh:
    coordHigh = (sizeGrid - sizeSquare + 1)
    for x in 1 .. coordHigh:
      for y in 1 .. coordHigh:
        # use squareTotalPower to avoid memoization
        power = squareTotalPowerMemo(x, y, serial, sizeSquare)
        if power > maxPower:
          maxPower = power
          xs = x
          ys = y
          sizeBest = sizeSquare
  echo xs, ",", ys, ",", sizeBest, " (", maxPower, ")"

var time = cpuTime()
const mySerial = 1309
solve(mySerial, 3, 3)
echo "Time taken: ", cpuTime() - time

# default compile
# Time taken: 1.203983
# with compile flag -d:release
# Time taken: 0.19564

# my first template
# in some blogs (e.g. Hookrace) you find stmt/expr instead of untyped/typed
template timeIt(body: untyped): untyped =
  # I need to have a time variable declared before
  time = cpuTime()
  body
  echo "Time taken: ", cpuTime() - time  

# part 2
echo "tests part 2"
timeIt solve(18, 3, 20)
timeIt solve(42, 3, 20)
echo "solution part 2"
timeIt solve(mySerial, 3, 20)
# times without memoization (but in d:release compile mode)
# tests part 2
# 90,269,16 (113)
# Time taken: 35.002495
# 232,251,12 (119)
# Time taken: 39.802366
# solution part 2
# 233,271,13 (108)
# Time taken: 47.442567

# times with memoization (and d:release mode!)
# tests part 2
# 90,269,16 (113)
# Time taken: 3.64298
# 232,251,12 (119)
# Time taken: 4.014614999999999
# solution part 2
# 233,271,13 (108)
# Time taken: 3.121841

# very nice, I see a 5-7x improvement over equivalent python version

# In principle in Nim I could add a compile flag to try with and without memoization with a minimal change to the code?
# in solve I would use when keyword, but for the pragmas how would it work??