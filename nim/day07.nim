let test_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
#1234567890123456789012345678901234567
#         1         2         3
#    * (5)                          *  (36)

import tables, strutils, algorithm, sequtils

# I would like nodes to be a set but then I do not find easy functions on it
proc process(text: string): (seq[char], Table[char, set[char]]) =
  var nodes: seq[char]
  var arrows = initTable[char, set[char]](1024)  
  var a, b: char
  # process input
  for line in text.splitLines():
      a = line[5]
      b = line[36]
      nodes.add(a)
      nodes.add(b)
      if arrows.hasKey(b):
        arrows[b].incl(a)
      else:
        arrows[b] = {a}
  return (nodes, arrows)

var nodes: seq[char]
var arrows: Table[char, set[char]]

(nodes, arrows) = process(test_input)    
echo nodes
echo arrows

# solve data
proc solve(nodes: var seq[char], arrows: var Table[char, set[char]]): seq[char] =
  var sequence: seq[char]
  var select: char
  var available: seq[char]
  var arrowsNew = initTable[char, set[char]](1024)
  while len(nodes) > 0:
    available = nodes.filterIt(not arrows.hasKey(it))
    select = sorted(available, system.cmp)[0]
    sequence.add(select)
    nodes.keepItIf(it != select)
    clear[char, set[char]](arrowsNew)
    for k, v in arrows:
      var v = v
      if select in v:
        v.excl(select)
      if card(v) > 0:
        arrowsNew[k] = v
    arrows = arrowsNew
  return sequence

var solution = solve(nodes, arrows)

echo solution.join("")

const input = readFile("./inputs/05.txt")

(nodes, arrows) = process(input)    
solution = solve(nodes, arrows)
echo solution.join("")