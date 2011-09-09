import random
import time
from collections import Counter

def create_deck():
	# create deck of cards
	# no suits just face values:
	# A K Q J 10 9 8 7 6 5 4 3 2
	deck = range(2,15)*4

	# shuffle (assuming that pseudo random is good enough)
	random.shuffle(deck)

	cut_size = len(deck)/2
	player1 = deck[:cut_size]
	player2 = deck[cut_size:]

	return player1, player2

def battle(player1, player2):
	# statistics
	game_stats['battle_count'] += 1

	# "each player draws a card, higher value card wins both"
	if player1[0] > player2[0]:
		pot = [player1[0],player2[0]]
		random.shuffle(pot)
		player1.extend(pot)
		del player1[0], player2[0]
		return

	if player1[0] < player2[0]:
		pot = [player1[0],player2[0]]
		random.shuffle(pot)
		player2.extend(pot)
		del player1[0], player2[0]
		return

	# "in the event of a tie, play a war"
	if player1[0] == player2[0]:
		ante = []
		ante.extend([player1[0],player2[0]])
		del player1[0], player2[0]
		war(player1, player2, ante)
		return

def war(player1, player2, ante):
	# statistics
	game_stats['war_count'] += 1
	game_stats['war_depth'] += 1

	# check that both players have sufficient cards for a war:
	if len(player1) < 3:
		player2.extend(ante+player1)
		return

	if len(player2) < 3:
		player1.extend(ante+player2)
		return

	# "each player antes three cards, then plays one of them"
	player1_draw = random.choice(player1[0:3])
	player2_draw = random.choice(player2[0:3])

	if player1_draw > player2_draw:
		pot = ante+player1[0:3]+player2[0:3]
		random.shuffle(pot)
		player1.extend(pot)
		del player1[0:3], player2[0:3]
		return

	if player1_draw < player2_draw:
		pot = ante+player1[0:3]+player2[0:3]
		random.shuffle(pot)
		player2.extend(pot)
		del player1[0:3], player2[0:3]
		return
	
	if player1_draw == player2_draw:
		ante.extend(player2[0:3]+player1[0:3])
		del player1[0:3], player2[0:3]
		war(player1, player2, ante)
		return


if __name__=='__main__':

	mark = time.time()
	stats = Counter()
	max_stats = Counter()
	number_of_runs = 100

	for run in range(1, number_of_runs):
		game_stats = Counter()
		player1, player2 = create_deck()

		while (len(player1) > 0) & (len(player2) > 0):
			battle(player1,player2)
			#print 'player1: ',player1
			#print 'player2: ',player2 , '\n'
			if game_stats['war_depth'] > 0:
				depth = game_stats['war_depth']
				game_stats['depth'+str(depth)] += 1
				game_stats['war_depth'] = 0
		
		# game level stats vs. simulation level stats
		for entry in game_stats:
			if game_stats[entry] > max_stats[entry]:
				max_stats[entry] = game_stats[entry]
			stats[entry] += game_stats[entry]

	# print stats
	print 'number_of_runs ', number_of_runs
	print 'time_elapsed ', time.time()-mark, '\n'
	stats += Counter() # clear zero counts
	max_stats += Counter()
	for entry in stats:
		print entry, stats[entry], stats[entry]/(number_of_runs*1.0)
	print '\n','max game stats'
	for entry in max_stats:
		print entry, max_stats[entry]
