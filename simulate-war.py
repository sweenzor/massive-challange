#! /usr/bin/python

import random
import time
from collections import Counter


class WarGame(object):
	"""Simulate the card game 'war'"""

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2

		while (len(player1.hand) > 0) & (len(player2.hand) > 0):

			battle(player1,player2)

		return None

	def battle(self):
		pass
	
	def war(self):
		pass

class Player(object):

	def __init__(self, hand):
		self.hand = hand
		return None

	def draw(self, number):
		draw = self.hand[0:number]
		del self.hand[0:number]
		return draw

	def return_cards(self, pot):
		random.shuffle(pot)
		self.hand.extend(pot)
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
	hand1, hand2 = Deck().deal()
	player1 = Player(hand1)
	player2 = Player(hand2)
	war = WarGame([player1,player2])
