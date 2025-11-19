import random

def get_winner():
    rand_a = random.randint(0,100)
    rand_b = random.randint(0,100)
    res = rand_a + rand_b
    return res

n = random.randint(3,5)
winners = []
for i in range(1,n):
    winner = get_winner()
    winners.append(winner)

print(winners)