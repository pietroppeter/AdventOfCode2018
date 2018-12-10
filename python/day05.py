test_input = "dabAcCaCBAcCcaDA"
with open('./inputs/05.txt') as f:
    my_input = f.read()

def match(a, b):
    if a.lower() == b.lower() and a != b:
        return True
    return False

print("xx", match("x", "x"))

def solve(s, verbose=0):
    i = 0
    if verbose == 1:
        print(''.join(s))
    while i < len(s) - 1:
        if match(s[i], s[i+1]):
            # print(i, s[i], s[i+1])
            if verbose == 2:
                print(f"{s[i]}{s[i+1]}")
            del s[i]
            del s[i]  # of course I should not do: del s[i+1]!! :)
            # print(s)
            if i > 0:
                i -= 1
            if verbose == 1:
                print(''.join(s))
        else:
            i += 1
sequence = list(test_input)
# print(sequence)
print(len(sequence))
solve(sequence)
print(''.join(sequence))
print(len(sequence))

# my input
sequence = list(my_input)
print(len(sequence))
solve(sequence)
print(len(sequence))

# my input - reduced
# sequence = list(my_input)[:100]
# print(len(sequence))
# solve(sequence, verbose=True)
# print(len(sequence))

# part 2
alphabet = list('abcdefghijklmnopqrstuvwxyz')
print(len(alphabet), ''.join(alphabet))

def solve2(text, verbose=0):
    min_len = 12_000
    min_char = '.'
    for c in alphabet:
        # print(c)
        new_input = text.replace(c, '')
        new_input = new_input.replace(c.upper(), '')
        if verbose > 0:
            print(new_input)
        new_input = list(new_input)
        solve(new_input, verbose=verbose)
        new_len = len(new_input)
        if verbose > 0:
            print(''.join(new_input))
        # print(new_len)
        if new_len < min_len:
            min_len= new_len
            min_char = c
    return min_char, min_len

print(solve2(test_input))
print(solve2(my_input))