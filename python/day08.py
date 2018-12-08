test_input = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

class node:

    def __init__(self, sequence):
        # reversed sequence of integer
        self.num_children = sequence.pop()
        self.num_meta = sequence.pop()
        self.children = list()
        for _ in range(self.num_children):
            self.children.append(node(sequence))
        self.meta = list()
        for _ in range(self.num_meta):
            self.meta.append(sequence.pop())

    def __repr__(self, tab=0):
        text = f"{tab*'  '}Node(num_children={self.num_children}, num_meta={self.meta}, meta={self.meta})"
        tab += 1
        for child in self.children:
            text += f"\n{child.__repr__(tab)}"
        return text

    def sum_metas(self):
        sum_metas = sum(self.meta)
        for child in self.children:
            sum_metas += child.sum_metas()
        return sum_metas
    # def __iter__(self):
    #     return self
    
    # def __next__(self):
    #     yield self
    #     for child in self.children:
    #         for node in child:
    #             yield node

sequence = test_input.split()
sequence.reverse()
sequence = list(map(lambda x: int(x), sequence))
root = node(sequence)
print(root)

# summing all metas
print(root.sum_metas())

# real case
# real case:
with open('./inputs/08.txt') as f:
    input = f.read()
sequence = input.split()
sequence.reverse()
sequence = list(map(lambda x: int(x), sequence))
root = node(sequence)
print(root.sum_metas())
