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
	
	def create(self):
		pass
	def deal(self):
		pass


class Card(object):
	"""Bare bones card class."""
	def __init__(self, value):
		self.value = value
		return None


if __name__ == "__main__":
	c = Card(1)
	print c.value