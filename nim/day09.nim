import strformat

# test inputs
var num_players = 9
var highest_marble = 25

# string are not immutable as in python! I can replace the index
var text = "hello"
echo text
text[1] = 'u'
echo text

type
  Circle = ref object
    marbles: seq[int]
    current: int

proc initCircle(): Circle =
  result = Circle(marbles: @[0], current: 0)  # I always need to initialize in this way?

var circle = initCircle()

proc `$`(c: Circle): string =
  for i, m in c.marbles:  # no need for enumerate
    if i == c.current:
      result &= fmt" ({m})"
    else:
      result &= fmt"  {m} "

echo circle

# I like the fact that I can spread the methods around (and test them one by one)
proc index(c: Circle, offset: int): int =
  result = (c.current + offset) mod c.marbles.len() + 1
  if result < 0:
    result += c.marbles.len

proc add(c: var Circle, marble: int, offset: int = 1) =
  c.current = c.index(offset)
  c.marbles.insert(marble, c.current)

for m in 1 .. 5:
  circle.add(m)
  echo circle

proc remove(c: var Circle, offset: int = -8): int =
  c.current = c.index(offset)
  # echo "removing at index ", c.current
  result = c.marbles[c.current]
  c.marbles.delete(c.current)

var removed: int
for m in 6 .. highest_marble:
  if m mod 23 == 0:
    echo "not adding ", m
    removed = circle.remove()
    echo "removed ", removed
  else:
    circle.add(m)
  echo circle

# I forgot to use Nim's convention for variables...
proc play(num_players, highest_marble: int): seq[int] =
  for i in 1 .. num_players:
    result.add(0)
  var current = 0
  var circle = initCircle()
  for m in 1 .. highest_marble:
    if m mod 23 == 0:
      # echo "not adding ", m
      # echo circle
      result[current] += m
      removed = circle.remove()
      result[current] += removed
    else:
      circle.add(m)
    current += 1
    if current == result.len:
      current = 0

var players = play(num_players, highest_marble)
echo players
echo players.max

let
  gamePlayers = @[10, 13, 17, 21, 30, 452]
  gameHighestMarbles = @[1618, 7999, 1104, 6111, 5807, 70784]

import times
var time = cpuTime()

for i in 0 .. gamePlayers.high:
  num_players = gamePlayers[i]
  highest_marble = gameHighestMarbles[i]
  time = cpuTime()
  players = play(num_players, highest_marble)
  echo fmt"{num_players} players; last marble is worth {highest_marble} points: high score is {players.max}"
  echo "time taken ", cpuTime() - time

# oddly enough my first correct nim version is much slower than python's version
# but I should compare with flag d:release

# part 2
num_players = gamePlayers[gamePlayers.high]
highest_marble = gameHighestMarbles[gameHighestMarbles.high]*100
echo fmt"{num_players} players; last marble is worth {highest_marble} points:"
time = cpuTime()
players = play(num_players, highest_marble)
echo fmt"{num_players} players; last marble is worth {highest_marble} points: high score is {players.max}"
echo "time taken ", cpuTime() - time
# compiled with flag d:release
# 1.5 secs
# *2: 5 secs (around *3 times)
# *4: 29 secs (around *6 times)
# *8: 96 secs (around *3 times than previous)
# estimate for *8*2*2*2*2=128 is 1.5 mins *3*3*3*3=81 is around 2 hours (or 16 times that...)
# what if I change the above to use array instead of sequences?