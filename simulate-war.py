#! /usr/bin/python

import random
import time
from collections import Counter

class Simulation(object):
	"""Run repeated games"""

	def __init__(self, runs):
		self.runs = runs
		return None

	def run(self):
		stats = Statistics()
		for i in range(self.runs):
			stats.game_new()
			hand1, hand2 = Deck().deal()
			player1 = Player(hand1)
			player2 = Player(hand2)
			war = Game(player1,player2, stats)
			stats.game_done()
		print stats
		return None


class Statistics(object):
	"""Record statistics on whole simulation and particular games"""

	def __init__(self):
		self.simulation_stats = Counter()
		self.game_stats = Counter()
		self.extrema_stats = Counter()
		return None
	
	def __str__(self):
		for entry in self.game_stats:
			print entry, self.game_stats[entry]
		return str()

	def game_new(self):
		pass

	def game_done(self):
		pass
	
	def load_depth(self):
		if self.game_stats['war_depth'] > 0:
			depth = self.game_stats['war_depth']
			self.game_stats['depth'+str(depth)] += 1
			self.game_stats['war_depth'] = 0
		return None

class Game(object):
	"""Simulate the card game 'war'"""

	def __init__(self, player1, player2, stats):
		self.player1 = player1
		self.player2 = player2
		self.stats = stats

		while (len(player1.hand) > 0) & (len(player2.hand) > 0):
			self.battle()

		return None

	def versus(self, player1_card, player2_card, ante):
		"""Card evaluator for either a war or battle"""
		# compare values of drawn cards
		if player1_card.value > player2_card.value:
			self.player1.return_cards(ante)
			return

		if player1_card.value < player2_card.value:
			self.player2.return_cards(ante)
			return

		# in the event of a tie, play a war
		if player1_card.value == player2_card.value:
			self.war(ante)
			return

		return None

	def battle(self):
		"""Battle"""
		# each player draws a card, higher value card wins both cards

		ante = []
		ante += self.player1.draw(1)
		ante += self.player2.draw(1)
		self.versus(ante[0], ante[1], ante)

		self.stats.game_stats['battles'] += 1 # statistics
		self.stats.load_depth() # statistics
		return None
	
	def war(self, ante):
		"""Wars are used to break ties during battles, can be recursive"""
		
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

		# begin war
		# "each player antes three cards, then plays one of them"
		draw1 = self.player1.draw(3)
		draw2 = self.player2.draw(3)
		ante += draw1 + draw2

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
		draw = self.hand[0:number]
		del self.hand[0:number]
		return draw

	def return_cards(self, ante):
		random.shuffle(ante)
		self.hand.extend(ante)
		return None

class Deck(object):
	"""Create deck of cards"""

	def __init__(self):
		"""Creating numerical value card deck"""
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
	A K Q J 10 9 8 7 6 5 4 3 2
	for simplicity of card comparison, we'll use numeric card values """

	def __init__(self, value):
		self.value = value
		return None

if __name__ == "__main__":
	mark = time.time()
	sim = Simulation(1000)
	sim.run()
	print 'time_elapsed ', time.time()-mark, '\n'

