import strutils, sequtils, algorithm, strformat, math

let test_input = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

proc process(text: string): seq[int] =
  reversed(text.split.map(parseInt))

var sequence: seq[int]

sequence = process(test_input)
echo test_input
echo sequence

type
  Node = ref object
    numChildren, numMetas: int
    children: seq[Node]
    metas: seq[int]

proc initNode(sequence: var seq[int]): Node =
  var node: Node
  # why do I need this initialization? without it the rest will not work
  result = Node(numChildren: 0, numMetas: 0, children: @[], metas: @[])
  result.numChildren = sequence.pop()
  result.numMetas = sequence.pop()
  result.children = @[]
  for i in 1 .. result.numChildren:
    result.children.add(initNode(sequence))
    result.metas = @[]
  for i in 1 .. result.numMetas:
    result.metas.add(sequence.pop())

var root = initNode(sequence)
echo root.numChildren
const tabStr = "  "

proc `$`(node: Node, tab: int = 0, deep: bool = true): string =
  result = ""
  for i in 1 .. tab:
    result &= "  "
  result &= fmt"Node(numChildren={node.numChildren}, numMetas={node.numMetas}, metas={node.metas})"
  if not deep:
    return result
  for child in node.children:
    result &= "\n" & `$`(child, tab + 1)
echo $root

proc sumMetas(node: Node): int =
  result += sum(node.metas)
  for child in node.children:
    result += child.sumMetas()

echo root.sumMetas()

proc value(node: Node): int =
  if node.numChildren == 0:
    return sum(node.metas)
  for i in node.metas:
    if 0 < i and i <= node.numChildren:
      result += node.children[i-1].value()

echo root.value()

# real case:
const input = readFile("./inputs/08.txt")
sequence = process(input)
root = initNode(sequence)
echo root.sumMetas()
echo root.value()
