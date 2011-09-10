#! /usr/bin/python

import random
import time
from collections import Counter


class WarGame(object):

	def battle(self):
		pass
	def war(self):
		pass

class Player(object):

	def draw(self):
		pass

class Deck(object):
	
	def __init__(self):
		"""Create deck of cards, no suits just face values:
		A K Q J 10 9 8 7 6 5 4 3 2"""
		
		self.deck = []
		for card_value in range(2,15)*4:
			self.deck.append(Card(card_value))

		# shuffle (assuming that pseudo random is good enough)
		random.shuffle(self.deck)

		return None

	def deal(self):
		# cut the deck
		cut_size = len(self.deck)/2
		sub_deck1 = self.deck[:cut_size]
		sub_deck2 = self.deck[cut_size:]

		# return the halved decks
		return sub_deck1, sub_deck2

class Card(object):
	"""Bare bones card class."""
	def __init__(self, value):
		self.value = value
		return None
	
	def __str__(self):
		return self.value


if __name__ == "__main__":
	d = Deck()
	a,b = d.deal()
	print len(a), len(b)