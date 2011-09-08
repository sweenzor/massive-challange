import random
import time

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

def battle(player1, player2):
	# "Each player draws a card, higher value card wins both"
	if player1[0] > player2[0]:
		player1.extend([player1[0],player2[0]])
		del player1[0], player2[0]
		return

	if player1[0] < player2[0]:
		player2.extend([player2[0],player1[0]])
		del player1[0], player2[0]
		return

	# "In the event of a tie, play a war"
	if player1[0] == player2[0]:
		ante = []
		ante.extend([player1[0],player2[0]])
		del player1[0], player2[0]
		war(player1, player2, ante)
		#check war count here
		return

def war(player1, player2, ante):
	# Check that both players have sufficient cards for a war:


	# "Each player antes three cards, then plays one of them"
	player1_draw = random.choice(player1[0:3])
	player2_draw = random.choice(player2[0:3])

	if player1_draw > player2_draw:
		player1.extend(ante+player1[0:3]+player2[0:3])
		del player1[0:3], player2[0:3]

	if player1_draw < player2_draw:
		player2.extend(ante+player2[0:3]+player1[0:3])
		del player1[0:3], player2[0:3]
	
	if player1_draw == player2_draw:
		ante.extend(player2[0:3]+player1[0:3])
		del player1[0:3], player2[0:3]
		war(player1, player2, ante)


mark = time.time()
player1, player2 = create_deck()
ante = []
while (len(player1) > 0) & (len(player2) > 0):
	battle(player1,player2)
	print 'player1: ',player1
	print 'player2: ',player2 , '\n'
print time.time()-mark