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

# I will have a set containing all shifts processed from input
class Shift:

    def __init__(self, id, date):
        self.id = id
        self.date = date
        # 0 index: asleep, 1 index: awake, 2: asleep, 3: awake, ...
        self.sleeps = list()
        self.events = 0
    
    def add_sleep_awake(minute, asleep=True):
        self.sleeps.append(minute)
        if asleep:
            self.events += 1


# I will also have a dictionary with all guard history (with id as key)
class GuardHistory:

    def __init__(self, id):
        self.id = id
        self.minutes = [0 for i in range(60)]
    
    def add_shift(shift):
        for event in range(shift.events):
            for m in range(shift.sleeps[2*event], shift.sleeps[2*event+1]):
                self.minutes[m] += 1


# processing test input
for line in test_input.split('\n'):
    print(line)
