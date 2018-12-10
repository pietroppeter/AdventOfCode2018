import sequtils, strutils

const testInput = "dabAcCaCBAcCcaDA"
const myInput = readFile("./inputs/05.txt")

proc match(a, b: char): bool =
  if a.toLowerAscii == b.toLowerAscii and a != b:
    return true
  return false

proc solve(s: var seq[char]) =
  var i = 0
  while i < s.len - 1:
    if s[i].match(s[i+1]):
      s.delete(i)  # watch out for del proc which does something different!
      s.delete(i)
      if i > 0:
        dec i
    else:
      inc i

var
  sequence: seq[char]

echo "test input"
sequence = toSeq(testInput.items)
echo sequence.len
solve(sequence)
echo sequence.join("")
echo sequence.len

echo "my input"
sequence = toSeq(myInput.items)
echo sequence.len
solve(sequence)
echo sequence.len
# takes much more time than python! why? because of the sequence?
# ah, possibly because of not doing it in release mode...

# part 2
const alphabet = toSeq("abcdefghijklmnopqrstuvwxyz".items)

proc solve2(text: string): int =
  var
    minLen = 12_000
    minChar = '.'
    newInput: string
    newInputSeq: seq[char]
    newLen: int
  
  for c in alphabet:
    newInput = text.replace($c, "")
    newInput = newInput.replace($(c.toUpperAscii), "")
    newInputSeq = toSeq(newInput.items)
    solve(newInputSeq)
    newLen = newInputSeq.len
    if newLen < minLen:
      minLen = newLen
      minChar = c
  echo minChar
  return minLen

echo solve2(testInput)
echo solve2(myInput)