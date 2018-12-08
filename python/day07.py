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
with open('./inputs/07.txt') as f:
    input = f.read()

nodes, arrows = process(input)
sequence = solve(nodes, arrows)
print(''.join(sequence))    

# part 2:
def time_to_complete(node, base_time=0):
    return base_time + ord(node) - ord('A') + 1

print('A', time_to_complete('A'))
print('C', time_to_complete('C'))

max_time = 10000

def parallel_solve(nodes, arrows, num_workers, base_time=0):
    todo = {e: 0 for e in nodes}
    done = []
    time = -1
    workers = [[] for i in range(num_workers)]
    while todo:
        # print("todo", todo)
        print("done", done)
        # print("arrows", arrows)
        time += 1
        if time >= max_time:
            break
        print("time", time)
        available = sorted([e for e in todo.keys() if todo[e] == 0 and e not in arrows.keys()], reverse=True)
        print("available", available)
        # assign nodes to worker not already working
        for i, worker in enumerate(workers):
            # print("worker", worker)
            # not already working
            if time + 1 != len(worker):
                # print("not working")
                # if there is a node available to process:
                if available:
                    worker.append(available.pop())
                    print("assigned", worker[-1], "to worker", i)
                else:
                    worker.append('.')
                    # print("goes idle")
                    continue
            # now it is for sure working on something
            something = worker[time]
            todo[something] += 1
            if todo[something] == time_to_complete(something, base_time=base_time):
                # if done on this node
                print("worker", i, "completed", something)
                todo.pop(something)
                done.append(something)
                arrows = {k: v - {something} if something in v else v for k, v in arrows.items() if something not in v or len(v) > 1}
            else:
                # if not done, next step I will still be working on this
                worker.append(something)
            # print(worker)
    return time + 1, done, workers

nodes, arrows = process(test_input)
time, done, workers = parallel_solve(nodes, arrows, num_workers=2)
print(time)
print(done)
print(workers)

print("\npart 2")
nodes, arrows = process(input)
print(nodes)
time, done, workers = parallel_solve(nodes, arrows, num_workers=5, base_time=60)
print(time)
print(done)
