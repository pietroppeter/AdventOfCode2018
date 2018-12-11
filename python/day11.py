import itertools

print("tests")
# serial 8
# cell 3, 5
# -> power level is 4
def hundred_digit(number):
    number = str(number)
    if len(number) > 2:
        return int(number[-3])
    else:
        return 0

print(hundred_digit(12))
print(hundred_digit(123))
print(hundred_digit(43210))
print(hundred_digit(4321))

def power_level(x, y, serial):
    rack_id = x + 10
    return hundred_digit((rack_id*y + serial)*rack_id) - 5

print(power_level(3, 5, 8))
# Here are some more example power levels:

# Fuel cell at  122,79, grid serial number 57: power level -5.
# Fuel cell at 217,196, grid serial number 39: power level  0.
# Fuel cell at 101,153, grid serial number 71: power level  4.
print(power_level(122, 79, 57), "== -5")
print(power_level(217, 196, 39), "== 0")
print(power_level(101, 153, 71), "== 4")

def square_total_power(x, y, serial):
    return sum([power_level(x + i, y + j, serial) for i in range(3) for j in range(3)])

# For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29); these fuel cells appear in the middle of this 5x5 region:

# -2  -4   4   4   4
# -4   4   4   4  -5
#  4   3   3   4  -4
#  1   1   2   4  -3
# -1   0   2  -5  -2

# For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30); they are in the middle of this region:

# -3   4   2   2   2
# -4   4   3   3   4
# -5   3   3   4  -4
#  4   3   3   4  -3
#  3   3   3  -5  -1

def example_plot(xs, ys, serial):
    print('\n'.join([''.join([f"{power_level(x, y, serial):4}" for x in range(xs - 1, xs - 1 + 5)]) for y in range(ys - 1, ys - 1 + 5)]))
    print(square_total_power(xs, ys, serial))

example_plot(33, 45, 18)
example_plot(21, 61, 42)

def solve(serial, size=300):
    max_power = -100
    xs, ys = None, None
    for x, y in itertools.product(range(1, size + 1 - 2), range(1, size + 1 - 2)):
        power = square_total_power(x, y, serial)
        if power > max_power:
            max_power = power
            xs, ys = x, y
    return max_power, xs, ys

print(solve(18, size=50))
print(solve(18, size=47))
print(solve(42, size=70))
print(solve(42, size=63))

my_serial = 1309
print("part 1 solution:", solve(my_serial))

# I want to use the memoize pattern (instead of setting up a grid) - to see how it changes and if it is possible in Nim:
def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func
