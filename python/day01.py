with open('./inputs/01.txt') as f:
    instructions = f.readlines()

changes = [int(line) for line in instructions]

def solve(changes, frequency=0, seen=None):
    seen = seen or {0}
    for change in changes:
        frequency += change
        if frequency in seen:
            return frequency
        else:
            seen.add(frequency)
    print('iterating again')
    return solve(changes, frequency=frequency, seen=seen)

print('part 1')
print(sum(changes))
print('part 2')
print(solve(changes))