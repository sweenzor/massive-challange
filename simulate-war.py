import random

def create_deck():
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

	return player1, player2

def battle(player1, player2):
	if player1[0] > player2[0]:
		player1.append(player1[0])
		player1.append(player2[0])
		del player1[0], player2[0]

	if player1[0] < player2[0]:
		player2.append(player2[0])
		player2.append(player1[0])
		del player1[0], player2[0]

	if player1[0] == player2[0]:
		war(player1, player2)


def war(player1, player2):
	# Each player antes three cards, then plays another card
	print random.choice(player1[1:4])
	print random.choice(player2[1:4])
	return cards



player1, player2 = create_deck()
while (len(player1) > 0) & (len(player2) > 0):

	print player1
	print player2