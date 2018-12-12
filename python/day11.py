import itertools
import time

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

# @memoize  # comment this line to have results without memoize
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

# @memoize  # comment this line to have results without memoize
def square_total_power(x, y, serial, size):
    if size <= 3:
        return sum([power_level(x + i, y + j, serial) for i in range(size) for j in range(size)])
    return square_total_power(x, y, serial, size - 1) \
           + sum([power_level(x + i, y + size - 1, serial) for i in range(size - 1)]) \
           + sum([power_level(x + size - 1, y + j, serial) for j in range(size)])

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
    print(square_total_power(xs, ys, serial, 3), xs, ys)

example_plot(33, 45, 18)
example_plot(21, 61, 42)

def solve(serial, size=300, size_square=None):
    if size_square is None:
        size_square = [3]
    max_power = -100
    xs, ys = None, None
    best_square_size = None
    for square in size_square:
        for x, y in itertools.product(range(1, size - square + 1), range(1, size  - square + 1)):
            power = square_total_power(x, y, serial, square)
            if power > max_power:
                max_power = power
                xs, ys = x, y
                best_square_size = square
    return max_power, xs, ys, best_square_size

print(solve(18, size=50))
print(solve(18, size=47))
print(solve(42, size=70))
print(solve(42, size=63))

my_serial = 1309
start = time.time()
print("\npart 1 solution:", solve(my_serial))
print("time taken: ", time.time() - start)
# a bit more than 1 second without memoize
# a bit less than 1 second with memoize
# I expected more of an improvement, but I guess that the function I am caching is already pretty fast

# part 2
# I have memoized also the squares
start = time.time()
print("\npart 2 test serial 18:", solve(18, size_square=list(range(3, 20))))
print("time taken: ", time.time() - start)

start = time.time()
print("\npart 2 test serial 42:", solve(42, size_square=list(range(3, 20))))
print("time taken: ", time.time() - start)

start = time.time()
print("\npart 2 my solution:", solve(my_serial, size_square=list(range(3, 20))))
print("time taken: ", time.time() - start)

# part 1 solution: (31, 20, 43, 3)
# time taken:  0.8248319625854492

# part 2 test serial 18: (113, 90, 269, 16)
# time taken:  17.45703935623169

# part 2 test serial 42: (119, 232, 251, 12)
# time taken:  21.266549110412598

# part 2 my solution: (108, 233, 271, 13)
# time taken:  23.892771005630493
