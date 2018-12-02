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
# echo countChars(test)
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

var twos = 0
var threes = 0
var hasTwo : bool
var hasThree : bool
echo len ids
for id in ids:
    clear(counter)
    # echo id
    for c in id:
      counter.inc(c)
    # echo counter
    hasTwo = false
    hasThree = false
    for k, v in counter:
      if v == 2:
        hasTwo = true
      elif v == 3:
        hasThree = true
    if hasTwo:
      twos += 1
    if hasThree:
      threes += 1
echo twos
echo threes
echo twos*threes

# second part

# distance bewteen ids
var id1 : string
var id2 : string
var dist : int

id1 = "abcde"
id2 = "axcye"
dist = 0
for i in 0..<id1.len:
  if id1[i] != id2[i]:
    dist += 1
echo dist
