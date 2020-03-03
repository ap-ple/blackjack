from os import system
import random
from stuff import *

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two' : 2, 'Three' : 3, 'Four' : 4, 'Five' : 5, 'Six' : 6, 'Seven' : 7, 'Eight' : 8, 'Nine' : 9, 'Ten' : 10, 'Jack' : 10, 'Queen' : 10, 'King' : 10, 'Ace' : 11}

class Card:

	def __init__(self, suit, rank, value):
		
		self.suit = suit
		self.rank = rank
		self.value = value

	def __str__(self):

		return f'{self.rank} of {self.suit}'

	def __repr__(self):

		return f'{self.rank} of {self.suit}'

	def __int__(self):

		return self.value

class Deck:
	
	def __init__(self):
			
			self.cards = []
			for suit in suits:
				for rank in ranks:
					self.cards.append(Card(suit, rank, values[rank]))

	def shuffle(self):
		
		random.shuffle(self.cards)

	def deal(self):
		
		return self.cards.pop(0)

class Hand:

	def __init__(self):
		
		self.cards = []
		self.value = 0
		self.aces = 0

	def add_card(self, card):
		
		self.cards.append(card)
		self.check_value()

	def check_value(self):

		self.value = 0
		for card in self.cards:
			self.value += card.value

	def adjust_for_ace(self):
		
		for card in self.cards:
			if card.value == 11 and self.value > 21:
				card.value = 1
				self.check_value()

class Chips:

	def __init__(self):
		
		self.total = 100
		self.bet = 0

	def win_bet(self):
		
		self.total += self.bet
    
	def lose_bet(self):
		
		self.total -= self.bet

def hit(deck, hand):
	hand.add_card(deck.deal())
	hand.adjust_for_ace()

def show_some(player, dealer):
	print("Dealer's Hand:")
	print(" <card hidden>")
	print(f' {dealer.cards[1]}')  
	print("\nPlayer's Hand:", *player.cards, sep='\n ')
	print(f"Player's Hand = {player.value}")

def show_all(player, dealer):
	print("Dealer's Hand:", *dealer.cards, sep='\n ')
	print(f"Dealer's Hand = {dealer.value}")
	print("\nPlayer's Hand:", *player.cards, sep='\n ')
	print(f"Player's Hand = {player.value}")

clear()
dialogue('Blackjack')
chips = Chips()

while True:
	playing = True
	deck = Deck()
	deck.shuffle()
	player = Hand()
	dealer = Hand()
	for i in range(2):
		hit(deck, player)
		hit(deck, dealer)
	while True:
		try:
			print(f'{chips.total} chips')
			chips.bet = int(dialogue('How many chips would you like to bet? '))
			if chips.bet > chips.total:
				print('error: insufficient chips')
				continue
			break
		except:
			print('error: invalid input')
	while playing:
		show_some(player, dealer)
		choice = dialogue('Hit or stand? ')
		if 'h' in choice or 'hit' in choice:
			hit(deck, player)
		elif 's' in choice or 'hit' in choice:
			playing = False
		else:
			print('error: invalid input')
		if player.value == 21:
			show_all(player, dealer)
			dialogue('Blackjack!')
			chips.total += chips.bet
			break
		elif player.value > 21:
			show_all(player, dealer)
			dialogue('Busted!')
			chips.total -= chips.bet
			break
	else:
		while dealer.value < 17:
			hit(deck, dealer)
		show_all(player, dealer)
		if dealer.value > 21:
			dialogue('Dealer busts, you win!')
			chips.total += chips.bet
		elif dealer.value > player.value:
			dialogue('Dealer wins.')
			chips.total -= chips.bet
		elif dealer.value == player.value:
			dialogue('Push.')
		else:
			dialogue('You win!')
			chips.total += chips.bet
	print(f'{chips.total} chips')
	dialogue('Play again?')