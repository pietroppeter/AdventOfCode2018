from collections import Counter

with open('./inputs/02.txt') as f:
    ids = f.readlines()

def count23(id):
    count = Counter(id)
    exactly_two = bool({k for k, v in count.items() if v == 2})
    exactly_three = bool({k for k, v in count.items() if v == 3})
    return exactly_two, exactly_three

def solve(ids):
    twos = 0
    threes = 0
    for id in ids:
        two, three = count23(id)
        twos += two
        threes += three
    return twos, threes

test = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""

test_ids = test.splitlines()

print(count23('bababc'))
a, b = solve(test_ids)
print(a, b, a*b)
a, b = solve(ids)
print(len(ids))
print(a, b, a*b)
