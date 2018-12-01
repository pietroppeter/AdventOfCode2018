# Learning: splitLines and parseInt from strutils, map from sequtils, sum from math
import strutils, sequtils, math

# Learning: built in set can only hold int8 or int16, but we need bigger ints for our input data
# Note that the error is seen already in visual code! I think this is because I am using const, nice!
# const changes = map(readFile("./inputs/01.txt").splitLines, proc(x: string): int16 = int16 parseInt(x))
# to manage any type (that can be hashed) into a set, there is HashSet
# also from gitter, I lerned there is also the option of IntSets (module intsets) - have not tried.
import sets
const changes = map(readFile("./inputs/01.txt").splitLines, proc(x: string): int = parseInt(x))

# watch out for some variables that need to be passed with var keyword. Also for multiple returns another options would have been (int, int)
proc solve(changes : seq[int], frequency : var int, seen : var HashSet[int], iterations : var int): tuple[frequency: int, iterations: int] =
  for change in changes:
    frequency += change
    if frequency in seen:
      return (frequency, iterations)
    else:
      seen.incl(frequency)
  inc iterations
  solve(changes, frequency, seen, iterations)

# Learning: this is not valid, the following is a valid way to initialize a HashSet (while for built-int sets this would have worked)
# const emptySet : HashSet[int] = {0}
var initialFrequency = 0
# the initialization size is crucial for performance: too small and the set will be continously recreated every time the size increase beyond the initial limit
var initialSet = initSet[int](2^17)  # weird that it accepts only powers of two, it could accept directly the log 2 of size, then.
initialSet.incl(initialFrequency)
var iterations = 0
var frequency : int

# Question: how do I do this? tried also $type(instructions) but it did not work!
# echo type(instructions)
# actually I can see the types in the IDE (Visual Code), so I should not be too worried about printing them... (I guess this is a Python reflex, where type can keep changing)
echo "part 1"
frequency = sum(changes)
echo "frequency: ", frequency
echo "part 2"
(frequency, iterations) =  solve(changes, initialFrequency, seen = initialSet, iterations = iterations)
echo "frequency: ", frequency, " iterations: ", iterations
