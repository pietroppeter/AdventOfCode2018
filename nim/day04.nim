# regular expressions in nim. there are (currently) 2 packages in stdlib: re and nre
# see: https://github.com/nim-lang/Nim/issues/7278
# let's try first re
import re, strutils

#                        0: day        1: hour 2: minute           3: id               4: asleep      5: awake   
let pattern = re"\[\d{4}-(\d{2}-\d{2}) (\d{2}):(\d{2})\] (?:Guard #(\d+) begins shift)?(falls asleep)?(wakes up)?"

var matches: array[6, string]

let test_input = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

# processing test input
for line in test_input.splitLines():
    echo line
    if match(line, pattern, matches):
      echo matches
# bizarre behaviour, last element of array is not reset when no match is given! ("wakes up" always appear after processing line 3!)

# I will do something different from python: a Table (similar to a python dict) of guards minutes
import tables, math

# not seeing in the documentation the fact that [A,B] refer to types of key, values of table
var guards = initTable[int, array[60, int]](1024)  # remember to set an adequate initial size!

var id, minute: int
var events: seq[int]
var minutes: array[60, int]

proc zero(minutes: var array[60, int]) =
  for i in minutes.low .. minutes.high:  # better way to zero again an array?
    minutes[i] = 0


proc update(minutes: var array[60, int], events: seq[int]) =
  for i in 0 ..< (events.len div 2):
    for j in events[2*i] ..< events[2*i + 1]:
      inc minutes[j]

minutes.update(@[5, 10])
echo minutes
minutes.update(@[5, 15])
echo minutes
zero(minutes)
echo minutes

proc process(text: string): Table[int, array[60, int]] =
  result = initTable[int, array[60, int]](1024)
  for line in text.splitLines():
    if not match(line, pattern, matches):
      echo "cannot understand this line: ", line
      continue
    if matches[3].len > 0:  # id: update guard table with last shift and create new shift
      if id != 0:  # first pass id is == 0
        # update guards
        if not guards.hasKey(id):
          zero(minutes)
          result[id] = minutes
        result[id].update(events)
      # create new shift data
      id = parseInt(matches[3])
      events = @[]
    else:
      events.add(parseInt(matches[2]))  # minute of other event

guards = process(test_input)

proc solve(guards: Table[int, array[60, int]]) =
  # guard with most minutes
  var idMax, totMins: int
  for id, minutes in guards:
    echo id, ": ", minutes.sum()
    if minutes.sum() > totMins:
      totMins = minutes.sum()
      idMax = id

  echo "guards with most minutes: ", idMax

  # minutes more often asleep
  var bestMinute, timesAsleep: int
  for minute in guards[idMax].low .. guards[idMax].high:
    if guards[idMax][minute] > timesAsleep:
      timesAsleep = guards[idMax][minute]
      bestMinute = minute

  echo "best minute: ", bestMinute
  echo "answer part 1: ", bestMinute*idMax

solve(guards)

# with real input:
import algorithm

const input = sorted(readFile("./inputs/04.txt").strip().splitLines(), system.cmp).join(sep="\n")

guards = process(input)
solve(guards)