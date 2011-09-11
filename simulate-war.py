#! /usr/bin/python

import random
import time
from collections import Counter

class Simulation(object):
	"""Run a game multiple times,
	record statistics on each game and the entire simulation"""

	def __init__(self, runs):
		self.runs = runs # number of times to run simulation
		self.stats = Statistics(self.runs)
		return None

	def __str__(self):
		print 'simulation statistics:\n'
		print self.stats
		print 'number of runs ', self.runs
		return str()

	def run(self):
		"""Initialize and run the game a specified number of times"""
		for i in range(self.runs):
			# create, shuffle and deal deck of cards
			hand1, hand2 = Deck().deal()
			player1 = Player(hand1)
			player2 = Player(hand2)

			# play the game of war
			war = Game(player1,player2, self.stats)

			# transition stats between individual game and sim at large
			self.stats.load_extrema()
			self.stats.load_simulation()
		return None


class Statistics(object):
	"""Record statistics on whole simulation and particular games"""

	def __init__(self, runs):
		"""Create Counter objects to record game information"""

		self.runs = runs # iterations of the sim, for averages
		self.simulation_stats = Counter()
		self.game_stats = Counter()
		self.extrema_stats = Counter()
		return None
	
	def __str__(self):
		self.simulation_stats += Counter()
		for entry in self.simulation_stats:
			print 'avg', entry, self.simulation_stats[entry]/float(self.runs)
		for entry in self.extrema_stats:
			print entry, self.extrema_stats[entry]
		return str()

	def game_new(self):
		"""Clear game level stats"""

		self.game_stats = Counter()
		return None
	
	def load_depth(self):
		"""Track the depth of recursion of 'wars'"""

		if self.game_stats['war_depth'] > 0:
			depth = self.game_stats['war_depth']
			self.game_stats['depth'+str(depth)] += 1
			self.game_stats['war_depth'] = 0
		return None

	def load_extrema(self):
		"""Track minimum and maximum values of game statistics
		across the entire simulation"""

		# check if the current game contains any 'record breaking' stats
		for entry in self.game_stats:
			if self.game_stats[entry] > self.extrema_stats['max '+entry]:
				self.extrema_stats['max '+entry] = self.game_stats[entry]

		# special case to record minimum value records
		if self.extrema_stats['min battles'] == 0:
			self.extrema_stats['min battles'] = self.game_stats['battles']
		if self.game_stats['battles'] < self.extrema_stats['min battles']:
			self.extrema_stats['min battles'] = self.game_stats['battles']

		return None

	def load_simulation(self):
		"""Add statistics from a game into simulation level statistics"""

		for entry in self.game_stats:
			self.simulation_stats[entry] += self.game_stats[entry]
		return None

class Game(object):
	"""Simulate the card game 'war'"""

	def __init__(self, player1, player2, stats):
		self.player1 = player1
		self.player2 = player2
		self.stats = stats

		# clear 'game level' stats
		self.stats.game_new()

		# continue to play battles until one player is out of cards
		while (len(player1.hand) > 0) & (len(player2.hand) > 0):
			self.battle()

		return None

	def versus(self, player1_card, player2_card, ante):
		"""General card evaluator for either a war or battle"""

		# compare values of drawn cards
		if player1_card.value > player2_card.value:
			self.player1.return_cards(ante)
			return

		if player1_card.value < player2_card.value:
			self.player2.return_cards(ante)
			return

		# in the event of a tie, play a war to break the tie
		if player1_card.value == player2_card.value:
			self.war(ante)
			return

		return None

	def battle(self):
		"""Battle between two players,
		each player draws a card, higher value card wins both cards"""

		# create pool to hold cards in play
		ante = []
		# add drawn cards into pool
		ante += self.player1.draw(1)
		ante += self.player2.draw(1)

		# compare the cards drawn by each player
		# in the event of a tie, a war will be played
		self.versus(ante[0], ante[1], ante)

		self.stats.game_stats['battles'] += 1 # statistics
		self.stats.load_depth() # statistics
		return None
	
	def war(self, ante):
		"""Wars are used to break ties during battles, can be recursive
		during a war, each player draws three cards, choses one of those
		three randomly, and plays those cards against each other"""
		
		# check that both players have sufficient cards for a war,
		# if not, sacrifice remaining cards to the victor
		if len(self.player1.hand) < 3:
			self.player2.hand.extend(ante+self.player1.hand)
			self.player1.hand = []
			return
		if len(self.player2.hand) < 3:
			self.player1.hand.extend(ante+self.player2.hand)
			self.player2.hand = []
			return

		# each player draws three cards, then plays one of them
		draw1 = self.player1.draw(3)
		draw2 = self.player2.draw(3)
		ante += draw1 + draw2 # add drawn cards into pool

		# randomly choose one of the three drawn cards to play
		draw1 = random.choice(draw1)
		draw2 = random.choice(draw2)
		
		# battle!
		self.versus(draw1, draw2, ante)

		self.stats.game_stats['war_depth'] += 1 # statistics
		self.stats.game_stats['wars'] += 1 # statistics
		return None


class Player(object):
	"""Player has hand from which they can draw cards,
	and return captured cards."""

	def __init__(self, hand):
		self.hand = hand
		return None
	
	def __str__(self):
		return str([card.value for card in self.hand])

	def __len__(self):
		return len(self.hand)

	def draw(self, number):
		"""Draw a number of cards from player hand,
		and pass them into play (remove them from hand)"""
		draw = self.hand[0:number]
		del self.hand[0:number]
		return draw

	def return_cards(self, ante):
		"""Accept cards from play and add them to player's hand
		cards are returned to the bottom of a players hand in a
		random order to prevent infinity looping games"""

		random.shuffle(ante)
		self.hand.extend(ante)
		return None

class Deck(object):
	"""Create deck of cards"""

	def __init__(self):
		"""Create numerical value card deck"""

		self.deck = []
		for card_value in range(2,15)*4:
			self.deck.append(Card(card_value))

		# shuffle deck in place, 
		# making the assumption that pseudo random is sufficient
		random.shuffle(self.deck)
		return None

	def deal(self):
		"""Cut the deck, making two evenly sized hands"""

		cut_size = len(self.deck)/2
		hand1 = self.deck[:cut_size]
		hand2 = self.deck[cut_size:]

		# return the halved deck
		return hand1, hand2

class Card(object):
	"""Bare bones card class. no suits just face values:
	A  K  Q  J  10 9 8 7 6 5 4 3 2
	14 13 11 12 10
	for simplicity of card comparison, we'll use numeric card values"""

	def __init__(self, value):
		self.value = value
		return None

if __name__ == "__main__":
	mark = time.time()
	
	runs = 100
	sim = Simulation(runs)
	sim.run()
	print sim

	run_time = time.time()-mark
	print 'time elapsed ', run_time
	print 'average time per run ', run_time/float(runs)
