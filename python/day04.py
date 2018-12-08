import re

# why this does not work
# pattern = re.compile('\[\d{4}-(?P<day>\d{2}-\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] (?:Guard #(\d+) begins shift)|(falls asleep)|(wakes up)')
# while this does?
pattern = re.compile('\[\d{4}-(?P<day>\d{2}-\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] (?:Guard #(?P<id>\d+) begins shift)?(?P<asleep>falls asleep)?(?P<awake>wakes up)?')

# how much easier would be to "compile" a func that produces a string given some inputs? it would be a different approach that re and maybe doable in Nim! (because of programmability)

test_input = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""
#123456789012345678901234567890
#         111111111122222222222
# I think I will need a regular expression here!

# processing test input
for line in test_input.split('\n'):
    print(line)
    match = pattern.search(line)
    if match is None:
        print('None')
    else:
        print({key: match.group(key) for key in 'day hour minute id asleep awake'.split()})


# I will have a set containing all shifts processed from input
class Shift:

    def __init__(self, id, date):
        self.id = id
        self.date = date
        # 0 index: asleep, 1 index: awake, 2: asleep, 3: awake, ...
        self.sleeps = list()
        self.events = 0
    
    def __repr__(self):
        return f"Shift(id={self.id}, date={self.date}, events={self.events}, sleeps={self.sleeps})"

    def add_sleep_awake(self, minute, asleep=True):
        self.sleeps.append(minute)
        if asleep:
            self.events += 1


# I will also have a dictionary with all guard history (with id as key)
class GuardHistory:

    def __init__(self, id):
        self.id = id
        self.minutes = [0 for i in range(60)]
    
    def __repr__(self):
        return f"Guard(id={self.id}, minutes={self.minutes})"

    def add_shift(self, shift):
        for event in range(shift.events):
            for m in range(shift.sleeps[2*event], shift.sleeps[2*event+1]):
                self.minutes[m] += 1
        return self



def process_input(text):
    shifts = set()
    guards = {}
    shift = None
    for line in text.split('\n'):
        if line == '':
            continue
        match = pattern.search(line)
        if match is None:
            raise ValueError('cannot process line:', line)
        if match.group('id'):
            # new shift, if there was a previous shift (if this is not the first one), update guard history
            if shift:
                shifts.add(shift)
                if shift.id in guards:
                    guards[shift.id].add_shift(shift)
                else:
                    guards[shift.id] = GuardHistory(shift.id).add_shift(shift)
            shift = Shift(id=match.group('id'), date=match.group('day'))
        elif match.group('asleep'):
            shift.add_sleep_awake(int(match.group('minute')))
        else:  # awake
            shift.add_sleep_awake(int(match.group('minute')), asleep=False)
        # update date if first date fell on day before
        if shift.date != match.group('day'):
            shift.date = match.group('day')
    return shifts, guards


shifts, guards = process_input(test_input)
print(shifts)
print(guards)

# Strategy 1 - test case
guards_by_minutes = {id: sum(guard.minutes) for id, guard in guards.items()}
print(guards_by_minutes)
guard_id = max(guards_by_minutes, key=guards_by_minutes.get)
print("Guard who spend the most minutes asleep", guard_id)
minutes = guards[guard_id].minutes
minute_max_asleep = max(range(len(minutes)), key=minutes.__getitem__)
print("Minute most asleep for guard", guard_id, ":", minute_max_asleep)
print("Solution: ", int(guard_id)*minute_max_asleep)

# Strategy 1 - real case
print("Real case:")
with open('./inputs/04.txt') as f:
    input = '\n'.join(sorted(f.readlines()))

shifts, guards = process_input(input)
guards_by_minutes = {id: sum(guard.minutes) for id, guard in guards.items()}
guard_id = max(guards_by_minutes, key=guards_by_minutes.get)
print("Guard who spend the most minutes asleep", guard_id)
minutes = guards[guard_id].minutes
minute_max_asleep = max(range(len(minutes)), key=minutes.__getitem__)
print("Minute most asleep for guard", guard_id, ":", minute_max_asleep)
print("Solution: ", int(guard_id)*minute_max_asleep)

# part 2
best_minute_by_guard = {id: max(range(len(guard.minutes)), key=guard.minutes.__getitem__) for id, guard in guards.items()}
best_guard = max(best_minute_by_guard, key=best_minute_by_guard.get)
best_minute = best_minute_by_guard[best_guard]
print("best guard: ", best_guard, "; its best minute: ", best_minute, "; their product: ", int(best_guard)*best_minute)