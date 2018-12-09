# test inputs
num_players = 9
highest_marble = 25

# replace string at index
def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

# circle of marbles
class Circle:

    def __init__(self):
        self.marbles = [0]
        self.current = 0  # index of current marble
    
    def _index(self, offset):
        return (self.current + offset) % len(self.marbles) + 1

    def add(self, marble, offset=1):
        self.current = self._index(offset)
        self.marbles.insert(self.current, marble)
    
    def remove(self, offset=-8):
        self.current = self._index(offset)
        removed = self.marbles[self.current]
        del self.marbles[self.current]
        return removed

    def __repr__(self):
        return ' '.join([f"({m})" if i == self.current else f" {m} " for i, m in enumerate(self.marbles)])

circle = Circle()
print(circle)
for m in range(1, highest_marble + 1):
    if m % 23 == 0:
        print("not adding", m)
        removed = circle.remove()
        print("removed", removed)
    else:
        circle.add(m)
    print(circle)

def play(num_players, highest_marble):
    players = [0 for i in range(num_players)]
    current = 0
    circle = Circle()
    for m in range(1, highest_marble + 1):
        if m % 23 == 0:
            players[current] += m
            removed = circle.remove()
            players[current] += removed
        else:
            circle.add(m)
        current += 1
        if current == len(players):
            current = 0
    return players

players = play(num_players, highest_marble)
print(players)
print(max(players))

game_players = [10, 13, 17, 21, 30, 452]
game_highest_marbles = [1618, 7999, 1104, 6111, 5807, 70784]
for num_players, highest_marble in zip(game_players, game_highest_marbles):
    players = play(num_players, highest_marble)
    print(f"{num_players} players; last marble is worth {highest_marble} points: high score is {max(players)}")

num_players = game_players[-1]
highest_marble = game_highest_marbles[-1]*10

# seems to be computationally unfeasible!
print("part 2")
players = play(num_players, highest_marble)
print(f"{num_players} players; last marble is worth {highest_marble} points: high score is {max(players)}")
