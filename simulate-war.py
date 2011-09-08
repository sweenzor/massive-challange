import random

def create_deck():
	# create deck of cards
	# no suits just face values:
	# A K Q J 10 9 8 7 6 5 4 3 2
	deck = range(2,15)*4

	# shuffle (assuming that pseudo random is good enough)
	random.shuffle(deck)

	#cut deck
	cut_size = len(deck)/2
	player1 = deck[:cut_size]
	player2 = deck[cut_size:]

	return player1, player2

def battle(player1, player2, ante):
	# "Each player draws a card, higher value card wins both"
	if player1[0] > player2[0]:
		player1.append(ante+player1[0]+player2[0])
		del player1[0], player2[0]

	if player1[0] < player2[0]:
		player2.append(ante+player2[0]+player1[0])
		del player1[0], player2[0]

	# "In the even of a tie, play a war"
	if player1[0] == player2[0]:
		ante.append(player1[0])
		ante.append(player2[0])
		war(player1, player2, ante)


def war(player1, player2, ante):
	# "Each player antes three cards, then plays another"
	player1_draw = player1[1:4]
	player2_draw = player2[1:4]

	battle(random.choice(player1[1:4]), random.choice(player1[1:4]))

	return cards



player1, player2 = create_deck()
ante = []
while (len(player1) > 0) & (len(player2) > 0):
	battle(player1,player2,ante)
	print player1
	print player2