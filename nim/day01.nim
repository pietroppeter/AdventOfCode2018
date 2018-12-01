# Learning: splitLines and parseInt from strutils, map from sequtils, sum from math
import strutils, sequtils, math

# Learning: built in set can only hold int8 or int16, but we need bigger ints for our input data (error is seen already visual code!)
# const changes = map(readFile("./inputs/01.txt").splitLines, proc(x: string): int16 = int16 parseInt(x))
# to manage any type (that can be hashed) into a set, there is HashSet
import sets
const changes = map(readFile("./inputs/01.txt").splitLines, proc(x: string): int = parseInt(x))

proc solve(changes : seq[int], frequency : var int, seen : var HashSet[int]): int =
  # I will use results as frequency variable
  for change in changes:
    frequency += change
    if frequency in seen:
      return frequency
    else:
      seen.incl(frequency)
  echo "iterating again"
  solve(changes, frequency, seen = seen)

# Learning: this is not valid, the following is a valid way to initialize a HashSet (while for built-int sets this would have worked)
# const emptySet : HashSet[int] = {0}
var initialFrequency = 0
var initialSet = initSet[int]()
initialSet.incl(initialFrequency)

# Question: how do I do this? tried also $type(instructions) but it did not work!
# echo type(instructions)
echo "part 1"
echo sum(changes)
echo "part 2"
echo solve(changes, initialFrequency, seen = initialSet)
# this solution is way slower than python! why?