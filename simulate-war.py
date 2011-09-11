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
			self.battle()
			print player1
			print player2, '\n'

		return None

	def versus(self, player1_card, player2_card, ante):
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

		return None
	
	def war(self, ante):
		"""Wars are used to break ties during battles, can be recursive"""
		
		# check that both players have sufficient cards for a war,
		# if not, sacrifice remaining cards to the victor
		if len(self.player1.hand) < 3:
			self.player2.hand.extend(ante+self.player1.hand)
			return

		if len(self.player2.hand) < 3:
			self.player2.hand.extend(ante+self.player1.hand)
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
		
		return None


class Player(object):
	"""Player has hand from which they can draw cards,
	and return capture cards too."""

	def __init__(self, hand):
		self.hand = hand
		return None
	
	def __str__(self):
		return str([card.value for card in self.hand])

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

class Statistics(object):
	pass

if __name__ == "__main__":
	hand1, hand2 = Deck().deal()
	player1 = Player(hand1)
	player2 = Player(hand2)
	war = WarGame(player1,player2)
