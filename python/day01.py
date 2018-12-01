with open('./inputs/01.txt') as f:
    instructions = f.readlines()

changes = [int(line) for line in instructions]

def solve(changes, frequency=0, seen=None, iterations=0):
    seen = seen or {0}
    for change in changes:
        frequency += change
        if frequency in seen:
            return frequency, iterations
        else:
            seen.add(frequency)
    iterations += 1
    return solve(changes, frequency=frequency, seen=seen, iterations=iterations)

print('part 1')
print(sum(changes))
print('part 2')
print(solve(changes))