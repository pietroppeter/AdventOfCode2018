# in Nim instead of using regular expression
# I will proceed with a simple for loop for parsing
# (I can use for loops without losing efficiency, yee!)

# let block and @ are the only changes need to go pyton -> nim here:
let
  claim1 = "#1 @ 1,3: 4x4"
  claim2 = "#2 @ 3,1: 4x4"
  claim3 = "#3 @ 5,5: 2x2"
  test_claims = @[claim1, claim2, claim3]

echo test_claims

# for parseInt
import strutils

# processing a single claim
# this will work only for claims with single digits
var groups : seq[int]
var i = 0
for c in claim1:
  case c:
    of ' ':
      continue
    of '#', '@', ',', ':', 'x':
      inc i
    else:
      groups.add(parseInt($c))
echo groups

# for map
import sequtils

# let's try to make it work with more complex claims:
let longer_claim = "#105 @ 90,423: 15x10"
echo longer_claim
var groupStr : seq[string]
i = -1
for c in longer_claim:
  case c:
    of ' ':
      continue
    of '#', '@', ',', ':', 'x':
      inc i
    else:
      if groupStr.len <= i:
        groupStr.add($c)
      else:      
        groupStr[i] = groupStr[i] & c
echo groupStr
groups = groupStr.map(parseInt)
echo groups

# Claim object
type
  Claim = ref object
    id*, x*, y*, w*, h*: int

var claim_obj : Claim

claim_obj = Claim(id: 105, x: 90, y: 423, w: 15, h: 10)

# equivalent to __repr__ (or __str__) of python
proc `$`(c: Claim): string =
  result = "Claim(id=" & $c.id & ", x=" & $c.x & ", y=" & $c.y & ", w=" & $c.w & ", h=" & $c.h & ")"

echo claim_obj

# now the code to process the claim text will become the equivalent of __init__ for Claim
proc initClaim(text: string): Claim =
  var groupStr : seq[string]
  var groupInt : seq[int]
  var i = -1
  for c in text:
    case c:
      of ' ':
        continue
      of '#', '@', ',', ':', 'x':
        inc i
      else:
        if groupStr.len <= i:
          groupStr.add($c)
        else:      
          groupStr[i] = groupStr[i] & c
  groupInt = groupStr.map(parseInt)
  # this is taken as return value
  Claim(id: groupInt[0], x: groupInt[1], y: groupInt[2], w: groupInt[3], h: groupInt[4])

echo initClaim(longer_claim)
for text in test_claims:
  echo initClaim(text)

# instead of creating an object where grid is seq[seq[int]], I can use directly a new type (see Matrix type in Nim by example):
type
  Tissue[size: static[int]] =
    array[size, array[size, int]]
# note the different syntax with respect to object definition
# reminder: refactor size to something else (see https://nim-lang.org/docs/apis.html)

# ... and also different initialization syntaz
var tissue: Tissue[7]
# since it is based on existing types it has automatic initialization and conversion to string
echo tissue

# ...but I want to override with a personal conversion to string

# first I need to understand how do I do the equivalent of join for strings in python...
# luckily it is join from strutils!
let s = @[@["1", "2"].join(), @["3", "4"].join()].join(sep="\n")
echo s
  
proc `$`(t: Tissue): string =
  var s: seq[string]
  for line in t:
    s.add(line.join())
  s.join(sep="\n")

# now $ is overridden
echo $tissue
echo tissue
echo tissue[0][0]

# method that changes the value of Tissue (note no return type is given):
proc add(t: var Tissue, c: Claim) =
  for y in c.y ..< c.y + c.h:
    for x in c.x ..< c.x + c.w:
      t[x][y] += 1

for claim in test_claims:
  echo claim
  tissue.add(initClaim(claim))
  echo tissue
echo tissue

proc countOverlaps(t: Tissue): int =
  # how to do a single for:
  for x in 0 ..< t.len:
    for y in 0 ..< t.len:
      if t[x][y] > 1: inc result

echo tissue.countOverlaps()

# now with the real data
const elfClaims = readFile("./inputs/03.txt").strip().splitLines()
var santasTissue: Tissue[1000]

for claim in elfClaims:
  santasTissue.add(initClaim(claim))
echo santasTissue.countOverlaps()