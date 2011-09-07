import random

# create deck of cards
# no suits just face values:
# A K Q J 10 9 8 7 6 5 4 3 2
deck = range(2,15)*4

# shuffle
random.shuffle(deck)

#cut deck
cut_size = len(deck)/2
player1 = deck[:cut_size]
player2 = deck[cut_size:]

print player1
print player2
