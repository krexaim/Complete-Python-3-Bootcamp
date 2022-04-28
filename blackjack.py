# -*- coding: utf-8 -*-
"""
Project 2: Blackjack

Created on Thu Apr 14 15:24:16 2022

@author: Alex
"""

import random

suits = ("Spades", "Hearts", "Diamonds", "Clubs")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':11, 'Queen':11, 'King':11, 'Ace':11}
playing = True


class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
class Deck():
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __repr__(self):
        currentdeck = ''
        for card in self.deck:
            currentdeck += "\n" + card.__str__()
        return currentdeck

    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        return self.deck.pop()
    
class Hand():
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("Place a bet: "))
        except ValueError:
            print("Value must be an integer.")
        else:
            if chips.bet > chips.total:
                print("Your balance is", chips.total, "choose a lower amount.")
            else:
                break

def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    
    global playing
    
    while True:
        x = input("Hit or stand? H or S: ")
        
        if x[0].lower() == "h":
            hit(deck,hand)
        elif x[0].lower() == "s":
            print("Stand. Dealer's turn.")
            playing = False
        else:
            print("Try again.")
            continue
        break
    
def show_some(player,dealer):
    print("\nDealer's Hand: \n <card hidden>", dealer.cards[1], "\n\n Player's Hand:", *player.cards, sep='\n')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n')
    print("Player's Hand =", player.value)
    
def player_busts(player,dealer,chips):
    print("Player bust")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins")
    chips.win_bet()
    
def dealer_busts(player,dealer,chips):
    print("Dealer bust")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins")
    chips.lose_bet()
    
def push(player,dealer):
    print("Push")
    
player_chips = Chips()
    
while True:
    print("Welcome to blackjack")
    
    #Create and shuffle deck
    deck = Deck()
    deck.shuffle()
    #Deal player and dealer hands
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    #Chip setup, take bet, show cards
    take_bet(player_chips)
    show_some(player_hand, dealer_hand)

    while playing:
        #Hit or stand
        hit_or_stand(deck,player_hand)
        
        show_some(player_hand,dealer_hand)
        
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        
        show_all(player_hand, dealer_hand)
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    print("\nYou have:", player_chips.total)
    
    if player_chips.total <= 0:
        print("You have no more chips to play with. Thanks for playing!")
        playing = False
        break
    
    new_game = input("Play again? y or n : \n")
    
    if new_game[0].lower() == 'y':
        print("\n")
        playing = True
        continue
    else:
        print("Thanks for playing")
        break
            
            
    