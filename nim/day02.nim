import tables, strutils

const ids = readFile("./inputs/02.txt").strip().splitLines()

var counter = initCountTable[char]()
var test = "abc"

proc countChars(text : string) : CountTable[char] =
  for c in text:
    echo c
    echo result
    result.inc(c)
    echo result

echo countChars(test)
echo ids[0]
# echo countChars(ids[0])
