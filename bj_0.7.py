

import pygame
import logging
from random import shuffle
from sys import exit
from os import system
from time import sleep


DECK_SIZE = 52
SUITE = ('C', 'D', 'H', 'S')
RANK = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Card:
    """
    
    """

    def __init__(self, index):
        self.suite = index//13
        self.rank = index % 13

    def __str__(self):
        return f"{SUITE[self.suite]}{RANK[self.rank]}"

    @property
    def BJ_Value(self):
        """Returns the cards value(2-11) in Blackjack."""
        value = self.rank + 1
        if value == 1:
            return 11
        return min(value, 10)


class Deck:
    """
    Deck is a list of cards to be popped.
    It stores unused, in-use, and used cards.
    """

    def __init__(self):
        self.cards = []
        self.discards = []
        self.in_use = []
        self.shoe_size = 1

    def Build(self, shoe=1):
        self.shoe_size = shoe
        self.cards.clear()
        self.discards.clear()
        self.in_use.clear()
        self.cards = [Card(i) for j in range(shoe) for i in range(DECK_SIZE)]
        shuffle(self.cards)

    def Deal(self, hand):
        card = self.cards.pop()
        logger.log(logging.DEBUG, f"Dealt card: {card}")
        self.in_use.append(card)
        hand.cards.append(card)

    def Discard(self, hand):
        self.in_use.clear()
        self.discards.extend(hand.cards)
        logger.log(logging.DEBUG, f"Hand cleared: {hand}")
        hand.Clear()

    def Count(self):
        known_cards = []
        known_cards.extend(self.discards)
        known_cards.extend(self.in_use)
        counts = []
        for i in range(13):
            counts.append(0)
        for card in known_cards:
            counts[card.rank] += 1
        print(counts, end=' ')
        print(sum(counts), end=' : ')
        count = 0
        # change placement of ace in the array (move to the back)
        for i in range(len(counts)):
            if i < 6 and not i == 0:
                count += counts[i]
            elif i == 6:
                count += counts[i] * 0.5
            elif i > 8 or i == 0:
                count -= counts[i]
        count += -2 * self.shoe_size
        print(count, end=' ')
        print(f'%{(count/(len(self.cards)/DECK_SIZE)):.2f}')
        sleep(5)


class Hand:
    """
    A class to manage a player's current hand and inform game logic per hand.
    """

    def __init__(self):
        self.cards = []
        self.bet = 0
        self.stand = False

    def __str__(self):
        h = ""
        for c in self.cards:
            h += c.__str__() + " "
        h += f" ({self.value})"
        if self.bet != 0:
            h += f" ${self.bet}"
        return h

    @property
    def value(self):
        ace = 0
        val = 0
        for c in self.cards:
            val += c.BJ_Value
            if c.BJ_Value == 11:
                ace += 1
        while ace > 0 and val > 21:
            val -= 10
            ace -= 1
        return val

    @property
    def bust(self):
        if self.value > 21:
            return True
        return False

    def Clear(self):
        self.cards.clear()
        self.bet = 0
        self.stand = False


class Player:
    """
    A class for profile data.
    """

    def __init__(self, name, bank):
        self.name = name
        self.bank = bank
        self.hands = []
        self.hands.append(Hand())

    def Clear(self):
        logging.log(logging.DEBUG, f"Player cleared: {self.name}")
        self.hands.clear()
        self.hands.append(Hand())

