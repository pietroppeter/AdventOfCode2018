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

# real case:
const input = readFile("./inputs/08.txt")
sequence = process(input)
root = initNode(sequence)
echo root.sumMetas()
#[

    def sum_metas(self):
        sum_metas = sum(self.meta)
        for child in self.children:
            sum_metas += child.sum_metas()
        return sum_metas
    # def __iter__(self):
    #     return self
    
    # def __next__(self):
    #     yield self
    #     for child in self.children:
    #         for node in child:
    #             yield node

sequence = test_input.split()
sequence.reverse()
sequence = list(map(lambda x: int(x), sequence))
root = node(sequence)
print(root)

# summing all metas
print(root.sum_metas())

# real case
# real case:
with open('./inputs/08.txt') as f:
    input = f.read()
sequence = input.split()
sequence.reverse()
sequence = list(map(lambda x: int(x), sequence))
root = node(sequence)
print(root.sum_metas())
]#