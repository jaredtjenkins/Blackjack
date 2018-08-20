

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
logger.setLevel(logging.WARNING)


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
        logging.log(logging.DEBUG, f"Player cleared: {player.name}")
        self.hands.clear()
        self.hands.append(Hand())


class Table:

    mode = 'menu'
    sub_mode = 'shoe'
    sim = False

    settings = {'shoe_size': 1,
                'minimum_bet': 10,
                'bj_payout': 1.5,
                'hit_soft_17': False}

    deck = Deck()
    deck.Build(shoe=settings['shoe_size'])

    dealer = Hand()

    players = []

    def Load_Settings(self):
        try:
            with open("settings") as f:
                x = f.readline()
        except:
            pass

    def Add_Player(self):
        name = 'Player'
        bank = 1000
        new_hand = Hand()
        new_player = Player(name, bank)
        self.players.append(new_player)

    def Remove_Player(self, player):
        self.players.pop(player)

    def Reset(self):
        pass

    def Sim(self, bet, rounds):
        #
        pass

    def Run(self):
        while True:

            if self.mode == 'quit':
                # save profile
                print("Goodbye")
                break

            elif self.mode == 'menu':
                system('cls')
                x = input(
                    '~~Welcome to CLI Blackjack~~\n(P)lay, (S)ettings, (Q)uit\n:')
                if x is 'p':
                    self.mode = 'play'
                elif x is 's':
                    self.mode = 'settings'
                elif x is 'q':
                    self.mode = 'quit'

            elif self.mode == 'settings':
                system('cls')

                if self.sub_mode == 'shoe':
                    x = input('Shoe Size (1-8): ')
                    try:
                        self.settings['shoe_size'] = int(x)
                    except ValueError:
                        continue
                    self.sub_mode = 'min'

                elif self.sub_mode == 'min':
                    x = input('Minimum Bet (1,): ')
                    try:
                        self.settings['minimum_bet'] = int(x)
                    except ValueError:
                        continue
                    self.sub_mode = 'soft'

                elif self.sub_mode == 'soft':
                    hit_soft_17 = input('Dealer hits soft 17 (y,n): ').lower()
                    if hit_soft_17 in ('t', 'true', 'y', 'yes'):
                        self.settings['hit_soft_17'] = True
                    else:
                        self.settings['hit_soft_17'] = False
                    self.sub_mode = 'payout'

                elif self.sub_mode == 'payout':
                    x = input('Blackjack payout (1.5, 2): ')
                    try:
                        self.settings['bj_payout'] = float(x)
                    except ValueError:
                        continue
                    self.sub_mode = 'default'

                elif self.sub_mode == 'default':
                    x = input('Save these settings as default (y,n): ').lower()
                    if x in ('t', 'true', 'y', 'yes'):
                        # save settings
                        pass
                    self.sub_mode = 'shoe'
                    self.mode = 'menu'

            elif self.mode == 'play':
                # get bet
                for player in self.players:
                    x = input(f'{player.name} ${player.bank} Bet: ')
                    try:
                        player.hands[0].bet = int(x)
                    except ValueError:
                        if x == 'q':
                            self.mode = 'quit'
                            continue
                        elif x == 'm':
                            self.mode = 'menu'
                            continue
                        elif x == '':
                            player.hands[0].bet = minimum_bet
                        else:
                            continue
                    if player.hands[0].bet < minimum_bet:
                        player.hands[0].bet = minimum_bet

                # deal cards
                for i in range(2):
                    deck.Deal(dealer)
                    for player in self.players:
                        deck.Deal(player.hands[0])

                # check for blackjacks, player plays if dealer doesn't have bj
                for player in self.players:
                    if dealer.value == 21 and player.hands[0].value != 21:
                        player.bank -= player.hands[0].bet
                    elif player.hands[0].value == 21:
                        player.hands[0].bet *= bj_payout
                    else:
                        Play(deck, player)

                # have dealer play
                while dealer.value < 17:
                    deck.Deal(dealer)

                # payout
                for player in self.players:
                    for hand in player.hands:
                        if hand.bust or (hand.value < dealer.value and not dealer.bust):
                            player.bank -= hand.bet
                        elif hand.value == dealer.value:
                            pass
                        else:
                            player.bank += hand.bet

                # round finished, show dealers hand
                Update_Display(flip=True)

                # collect all cards
                for player in self.players:
                    for hand in player.hands:
                        deck.Discard(hand)
                deck.Discard(dealer)

                # reset hands
                dealer.Clear()
                for player in self.players:
                    player.hands.clear()
                    player.hands.append(Hand())

                # reset deck if past certain point
                if len(self.deck.discards) > (DECK_SIZE * self.settings['shoe_size']) * 3/4:
                    self.deck.Build(self.settings['shoe_size'])


def Update_Display(flip=False):
    """
    Prints and formats all the current data into a readable string. 
    """

    # system('cls')

    print('Dealer:', end=' ')
    if not flip and dealer.value != 21:
        print('X', end='  ')
        print(dealer.cards[-1])
    else:
        print(dealer)

    print('Player:', end=' ')
    if len(player.hands) == 1:
        print(player.hands[0])
    else:
        print()
        for hand in player.hands:
            print(f"    #{player.hands.index(hand)+1}", end=' ')
            print(hand)


def Play(deck, player, sim=False):
    """
    A recursive function that handles input and modifies player hands 
    """

    for hand in player.hands:
        while not hand.bust and not hand.stand:
            # Update_Display()

            if not sim:
                Update_Display()
                if len(player.hands) == 1:
                    move = input(':')
                else:
                    move = input(f'#{player.hands.index(hand)+1}: ')
                if move == 'sim':
                    sim = True

            if sim:
                move = Basic(dealer, hand)
                logger.log(logging.DEBUG, f"sim move: {move}")

            if move == 's' or move == '':
                hand.stand = True
                continue

            elif move == 'h':
                deck.Deal(hand)
                continue

            elif move == 'd':
                if len(hand.cards) > 2:
                    continue
                hand.bet *= 2
                deck.Deal(hand)
                hand.stand = True
                continue

            elif move == 'sp':
                if len(player.hands) == 4 or len(hand.cards) < 2:
                    continue
                new_hand = Hand()
                new_hand.bet = hand.bet
                new_hand.cards.append(hand.cards.pop())
                player.hands.append(new_hand)
                Play(deck, player)
                continue

            elif move == 'c':
                deck.Count()


def Basic(dealer, player):

    # map hand to chard
    # e.g. Dealer: H7 Player: S9 h8 (17)
    #    2 3 4 5 6 7 8 9 X A
    # 16 0 0 0 0 0 1 1 1 1 1
    # 15 0 0 0 0 0 1 1 1 1 1
    # 14 0 0 0 0 0 1 1 1 1 1
    # 13 0 0 0 0 0 1 1 1 1 1
    # 12 1 1 0 0 0 1 1 1 1 1

    if player.value == 11:
        if len(player.cards) == 2:
            return 'd'
        return 'h'

    if player.value < 11:
        return 'h'

    if dealer.cards[-1].BJ_Value > 6 and player.value < 17:
        return 'h'
    elif dealer.cards[-1].BJ_Value < 4 and player.value == 12:
        return 'h'
    else:
        return 's'


if __name__ == '__main__':
    mode = 'menu'
    sub_mode = 'shoe'
    rounds = 0

    shoe_size = 1
    minimum_bet = 1
    bj_payout = 1.5
    hit_soft_17 = False

    dealer = Hand()
    player = Player('Player', 5000)

    deck = Deck()
    deck.Build(shoe_size)

    while True:

        if mode == 'quit':
            # save profile
            print("Goodbye " + player.name)
            break

        elif mode == 'menu':
            #system('cls')
            x = input(
                '~~Welcome to CLI Blackjack~~\n(P)lay, (S)ettings, (Q)uit\n:')
            if x == 'p':
                mode = 'play'
            elif x == 's':
                mode = 'settings'
            elif x == 'q':
                mode = 'quit'
            elif x == 'sim':
                rounds = int(input('Rounds: '))
                mode = 'sim'

        elif mode == 'pause':
            x = input('press any key to resume')
            mode = 'sim'

        elif mode == 'settings':
            #system('cls')

            if sub_mode == 'shoe':
                x = input('Shoe Size (1-8): ')
                try:
                    shoe_size = int(x)
                except ValueError:
                    continue
                sub_mode = 'min'

            elif sub_mode == 'min':
                x = input('Minimum Bet (1,): ')
                try:
                    minimum_bet = int(x)
                except ValueError:
                    continue
                sub_mode = 'soft'

            elif sub_mode == 'soft':
                hit_soft_17 = input('Dealer hits soft 17 (y,n): ').lower()
                if hit_soft_17 in ('t', 'true', 'y', 'yes'):
                    hit_soft_17 = True
                else:
                    hit_soft_17 = False
                sub_mode = 'payout'

            elif sub_mode == 'payout':
                x = input('Blackjack payout (1.5, 2): ')
                try:
                    blackjack_payout = float(x)
                except ValueError:
                    continue
                sub_mode = 'default'

            elif sub_mode == 'default':
                x = input('Save these settings as default (y,n): ').lower()
                if x in ('t', 'true', 'y', 'yes'):
                    # save settings
                    pass
                sub_mode = 'shoe'
                mode = 'menu'

        elif mode == 'play':

            # get bet
            x = input(f'{player.name} ${player.bank} Bet: ')
            try:
                player.hands[0].bet = int(x)
            except ValueError:
                if x == 'q':
                    mode = 'quit'
                    continue
                elif x == 'm':
                    mode = 'menu'
                    continue
                elif x == '':
                    player.hands[0].bet = minimum_bet
                else:
                    continue

            if player.hands[0].bet < minimum_bet:
                player.hands[0].bet = minimum_bet

            # deal cards
            for i in range(2):
                deck.Deal(dealer)
                deck.Deal(player.hands[0])

            # check for blackjacks, player plays if dealer doesn't have bj
            if dealer.value == 21 and player.hands[0].value != 21:
                player.bank -= player.hands[0].bet
            elif player.hands[0].value == 21:
                player.hands[0].bet *= bj_payout
            else:
                Play(deck, player)

            # have dealer play
            while dealer.value < 17:
                deck.Deal(dealer)

            # payout
            for h in player.hands:
                if h.bust or (h.value < dealer.value and not dealer.bust):
                    player.bank -= h.bet
                elif h.value == dealer.value:
                    pass
                else:
                    player.bank += h.bet

            # round finished, show dealers hand
            Update_Display(flip=True)

            # collect all cards
            for h in player.hands:
                deck.Discard(h)
            deck.Discard(dealer)

            # reset hands
            deck.Discard(dealer)
            for h in player.hands:
                deck.Discard(h)
            player.Clear()

            # reset deck if past certain point
            if len(deck.discards) > (DECK_SIZE * shoe_size) * 3/4:
                deck.Build(shoe_size)

        elif mode == 'sim':
            for r in range(rounds):
                logger.log(logging.DEBUG, f"sim round: {r}")
                player.hands[0].bet = minimum_bet

                for j in range(2):
                    deck.Deal(dealer)
                    deck.Deal(player.hands[0])

                if dealer.value == 21 and player.hands[0].value != 21:
                    player.bank -= player.hands[0].bet
                elif player.hands[0].value == 21:
                    player.hands[0].bet *= bj_payout
                else:
                    Play(deck, player, sim=True)

                # payout
                for h in player.hands:
                    if h.bust or (h.value < dealer.value and not dealer.bust):
                        player.bank -= h.bet
                    elif h.value == dealer.value:
                        pass
                    else:
                        player.bank += h.bet

                # collect all cards
                for hand in player.hands:
                    deck.Discard(hand)
                deck.Discard(dealer)
                player.Clear()

                # reset deck if past certain point
                if len(deck.discards) > (DECK_SIZE * shoe_size) * 3/4:
                    deck.Build(shoe_size)

            print(f'${player.bank-5000}')
            mode = 'menu'
