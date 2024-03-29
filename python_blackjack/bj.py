
from random import shuffle
from os import system, path

DECK_SIZE = 52
SUITE = ('C', 'D', 'H', 'S')
RANK = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
DATA = "data.txt"

class Card:

    def __init__(self, index):
        self.suite = index // 13
        self.rank = index % 13

    def __str__(self):
        return f"{SUITE[self.suite]}{RANK[self.rank]}"


class Deck:

    def __init__(self):
        # cards in the deck
        self.cards = []
        # number of decks
        self.shoe = 1

    def Build(self, shoe=1):
        self.shoe = shoe
        self.cards.clear()
        self.cards = [Card(i) for j in range(shoe) for i in range(DECK_SIZE)]
        shuffle(self.cards)


class Hand():
    def __init__(self):
        # the list of cards
        self.cards = []
        # the bet for this hand
        self.bet = 0
        # the value of this hand
        self.value = 0

    def Clear(self):
        self.cards.clear()
        self.bet = 0
        self.value = 0

    def Update_Value(self):
        val, ace = 0, 0
        for c in self.cards:
            if c.rank == 0:
                val += 11
                ace += 1
            else:
                val += min(c.rank + 1,10)
            if val > 21 and ace > 0:
                val -= 11
                ace -= 1
        self.value = val

    def __str__(self):
        string = ""
        for c in self.cards:
            string += f" {SUITE[c.suite]}{RANK[c.rank]}"                       
        string += f" ({self.value}) "
        return string


class Player():
    def __init__(self):
        # counter of wins-losses
        self.money = 0
        # a list of hands, used to support splitting a hand
        self.hands = []


def Dump():
    system('cls')
    print("Dealer: ")
    print(dealer)
    for player in players:
        print("Player: ")
        for hand in player.hands:
            if len(player.hands) != 1:
                print(f"#{player.hands.index(hand)+1}",end="")
            print(hand)


def loop():
    playing = True
    while playing:

        #get player bets
        for player in players:
            for hand in player.hands:
                hand.bet = 1 #int(input(f"Bet: "))

        #deal to active players
        for i in range(2):
            dealer.cards.append(deck.cards.pop())
            for player in players:
                for hand in player.hands:
                    if hand.bet:
                        hand.cards.append(deck.cards.pop())

        #calc hand values
        dealer.Update_Value()   
        for player in players:
            for hand in player.hands:
                hand.Update_Value()
        Dump()
        #check for blackjack
        for player in players:
            for hand in player.hands:
                if hand.value == 21:
                    hand.bet *= 1.5

        #each player plays hand
        if dealer.value != 21:
            for player in players:
                for hand in player.hands:
                    while hand.value <= 21:
                        state = input(": ")
                        if state == 's':
                            break
                        elif state == 'h':
                            hand.cards.append(deck.cards.pop())
                            hand.Update_Value()
                        elif state == 'd':
                            if len(hand.cards) > 2:
                                continue
                            hand.cards.append(deck.cards.pop())
                            hand.bet *= 2
                            hand.Update_Value()
                            break
                        elif state == 'sp':
                            if len(hand.cards) != 2:
                                continue
                            player.hands.append(Hand())
                            player.hands[-1].cards.append(hand.cards.pop())
                            player.hands[-1].Update_Value()
                            hand.Update_Value()
                        Dump()

        #dealer play:
        while dealer.value < 17:
            dealer.cards.append(deck.cards.pop())
            dealer.Update_Value()
        Dump()
        #payout
        for player in players:
            for hand in player.hands:
                if hand.value < dealer.value:
                    player.money -= hand.bet
                elif hand.value > dealer.value:
                    player.money += hand.bet
            player.hands.clear()
            player.hands.append(Hand())            
        dealer.Clear()
    
        #check shuffle(deck penetration)
        if len(deck.cards) < (DECK_SIZE * deck.shoe * 0.25):
            deck.Build()         


if __name__ == '__main__':

    deck = Deck()
    deck.Build()
    dealer = Hand()
    players = []
    players.append(Player())
    for player in players:
        player.hands.append(Hand())

    loop()