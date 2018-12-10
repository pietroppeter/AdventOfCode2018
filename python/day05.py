test_input = "dabAcCaCBAcCcaDA"
with open('./inputs/05.txt') as f:
    my_input = f.read()

# in python I have to convert to list, in nim probably I don't
sequence = list(test_input)

def match(a, b):
    if a.lower() == b or a.upper() == b:
        return True
    return False

def solve(s):
    i = 0
    while i < len(sequence) - 1:
        if match(s[i], s[i+1]):
            # print(i, s[i], s[i+1])
            del s[i]
            del s[i]  # of course I should not do: del s[i+1]!! :)
            # print(s)
            if i > 0:
                i -= 1
        else:
            i += 1
# print(sequence)
solve(sequence)
print(''.join(sequence))
print(len(sequence))

# my input
sequence = list(my_input)
solve(sequence)
print(len(sequence))
