import tables, strutils

var counter = initCountTable[char]()
var test = "abc"

echo counter
for c in test:
  echo c
  counter.inc(c)
  echo counter
echo counter

proc countChars(text : string) : CountTable[char] =
  echo result
  for c in text:
    echo c
    result.inc(c)
    echo result

# this throws an error and I cannot understand why!
echo countChars(test)
#[ output:
{:}
a
{'a': 1}
b
{'a': 1, 'b': 1}
c
{'a': 1, 'b': 1, 'c': 1}
{'a': 1, 'b': 1, 'c': 1}
{:}
a
day02.nim(22)            day02
day02.nim(19)            countChars
tables.nim(1004)         inc
system.nim(414)          rawGet
system.nim(2830)         sysFatal
Error: unhandled exception: index out of bounds [IndexError]
Error: execution of an external program failed: 'C:\Users\ppeterlongo\Documents\nim\AdventOfCode2018\nim\day02.exe '
]#

const ids = readFile("./inputs/02.txt").strip().splitLines()

echo ids[0]
# echo countChars(ids[0])
