test_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
#1234567890123456789012345678901234567
#         1         2         3
#    * (5)                          *  (36)

def process(text):
    nodes = set()
    arrows = {}
    for line in text.split('\n'):
        a = line[5]
        b = line[36]
        nodes = nodes.union({a, b})
        if b in arrows:
            arrows[b].add(a)
        else:
            arrows[b] = {a}
    return nodes, arrows

nodes, arrows = process(test_input)
print(nodes)
print(arrows)

def solve(nodes, arrows):
    sequence = []
    while nodes:
        select = sorted([e for e in nodes if e not in arrows.keys()])[0]
        sequence.append(select)
        nodes.remove(select)
        arrows = {k: v - {select} if select in v else v for k, v in arrows.items() if select not in v or len(v) > 1}
    return sequence

sequence = solve(nodes, arrows)

print(''.join(sequence))    

# real case:
with open('./inputs/05.txt') as f:
    input = f.read()

nodes, arrows = process(input)
sequence = solve(nodes, arrows)
print(''.join(sequence))    

