# In this day I will make use of objects in Python
# in this way I hope to learn the equivalent for Nim

# regular expresion are used to parse the claim
import re

pattern = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

# test cases
claim1 = "#1 @ 1,3: 4x4"
claim2 = "#2 @ 3,1: 4x4"
claim3 = "#3 @ 5,5: 2x2"
test_claims = [claim1, claim2, claim3]

# testing the regular expression is working
for claim in test_claims:
    print(claim)
    match = pattern.match(claim)
    print(match.groups())

# output:
"""
#1 @ 1,3: 4x4
('1', '1', '3', '4', '4')
#2 @ 3,1: 4x4
('2', '3', '1', '4', '4')
#3 @ 5,5: 2x2
('3', '5', '5', '2', '2')
"""

# a claim object to hold the claim of each elf
class Claim:

    def __init__(self, text):
      match = pattern.match(text)
      self.id = int(match.group(1))
      self.x = int(match.group(2))
      self.y = int(match.group(3))
      self.w = int(match.group(4))
      self.h = int(match.group(5))

    def __repr__(self):
      return f'Claim(id={self.id}, x={self.x}, y={self.y}, w={self.w}, h={self.h})'
    
# test the claim object
for claim in [claim1, claim2, claim3]:
    print(claim)
    claim_obj = Claim(claim)
    print(claim_obj)

# output:
"""
#1 @ 1,3: 4x4
Claim(id=1, x=1, y=3, w=4, h=4)
#2 @ 3,1: 4x4
Claim(id=2, x=3, y=1, w=4, h=4)
#3 @ 5,5: 2x2
Claim(id=3, x=5, y=5, w=2, h=2)
"""

# use a tissue "matrix" to count how many claims insist on each square inch of the grid
# I want to go with basic python, so I will avoid numpy (but I will miss the slicing on both indices)
# (also, I am working offline on a train on a new windows laptop on which numpy build is broken...)
class Tissue:

    def __init__(self, size=7):
        # always square
        self.size = size 
        self.grid = [[0 for x in range(size)]  for y in range(size)]
    
    def __repr__(self):
        return '\n'.join([''.join([str(i) for i in line]) for line in self.grid])

    def add(self, claim):
        # since I do not have numpy slicing capabilities I need a for loop over lines:
        for y in range(claim.y, claim.y + claim.h):
            # not only that, since I do not have a simple +1 on a list I need to loop over columns too!
            for x in range(claim.x, claim.x + claim.w):
                self.grid[x][y] += 1
    
    def overlap_coordinates(self):
        return [(x, y) for x in range(len(self.grid))
                       for y in range(len(self.grid[x]))
                       if self.grid[x][y] > 1]


# test tissue:
tissue = Tissue()
print(tissue)

for claim in test_claims:
    print(claim)
    tissue.add(Claim(claim))
    print(tissue)

# finally I can output the number of contested square inches:
print("overlapping square inches: ", len(tissue.overlap_coordinates()))

# output:
"""
0000000
0000000
0000000
0000000
0000000
0000000
0000000
#1 @ 1,3: 4x4
0000000
0001111
0001111
0001111
0001111
0000000
0000000
#2 @ 3,1: 4x4
0000000
0001111
0001111
0112211
0112211
0111100
0111100
#3 @ 5,5: 2x2
0000000
0001111
0001111
0112211
0112211
0111111
0111111
overlapping square inches: 4
"""

# now let's process the real input:
with open('./inputs/03.txt') as f:
    claims = f.readlines()

tissue = Tissue(size=1000)

for claim in claims:
    tissue.add(Claim(claim))

# finally I can output the number of contested square inches:
print("overlapping square inches: ", len(tissue.overlap_coordinates()))

### second part

# find non overlapping coordinates and lengths
grid = tissue.grid
x, y = min([(x, y) for x in range(len(grid)) for y in range(len(grid[x])) if grid[x][y] == 1])
print(x, y)
# I do not atcually need to find w and h! The following formulas do not give me the correct w and h!
w = max([w for w in range(1000 - x) if grid[x + w][y] == 1])
h = max([h for h in range(1000 - y) if grid[x][y + h] == 1])
print(w, h)
# print(tissue)

# find non overlapping id
for claim in claims:
    c = Claim(claim)
    # if c.x == x and c.y == y and c.w == w and c.h == h:
    if c.x == x and c.y == y:  # since it does not overlap I am guaranteed to find only one claim id
        print(c.id)
        break
print(claim)

# wrong answer.
# let's go simpler. we reprocess all claims:
for claim in claims:
    c = Claim(claim)
    if all([grid[c.x + w][c.y + h] == 1 for w in range(c.w) for h in range(c.h)]):
        print(c)
        break