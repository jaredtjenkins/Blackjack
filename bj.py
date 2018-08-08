import random
import sys
import os

DECK_SIZE = 52
SUITE = ('C','D','H','S')
VALUE = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')

def Print_Card(card):
    print(SUITE[card//13],end='')
    print(VALUE[card%13],end='')
    print('',end=' ')

# holds a list of cards and has a value and other convient metadeta
class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.bet = 0
        self.prev_bet = 0
        self.stand = False
        self.bust = False

    def Update_Value(self):
        ace = 0
        val = 0
        for c in self.cards:
            face_value = c%13 + 1
            if face_value == 1:
                ace += 1
                val += 11
            elif face_value > 10:
                val += 10
            else:
                val += face_value
        while ace > 0 and val > 21:
            val -= 10
            ace -= 1
        self.value = val

    def Add_Card(self, card):
        self.cards.append(card)
        self.Update_Value()
        if self.value > 21:
            self.bust = True

    def Remove_Card(self):
        card = self.cards.pop()
        self.Update_Value()
        return card

# holds name, money, and current cards in a list of card list called hands
class Player():
    def __init__(self, name = '', bank = 0, hand = Hand()):
        self.name = name
        self.bank = bank
        self.hands = []
        self.hands.append(hand)

    def Load_Profile(self, name):
        pass

    def Save_Profile(self):
        pass

# handles all printing except for input prompts
def Update_Display(flip = False):
    os.system('cls')
    print('Dealer:',end=' ')
    if not flip:
            print('X',end=' ')
            Print_Card(dealer.hands[0].cards[len(dealer.hands[0].cards)-1])
            print('')
    else:
        for c in dealer.hands[0].cards:
                Print_Card(c)
        print('({})'.format(dealer.hands[0].value))

    print('{}:'.format(player.name),end=' ')
    if len(player.hands) == 1:
        for c in player.hands[0].cards:
            Print_Card(c)
        print('({}) ${}'.format(player.hands[0].value, player.hands[0].bet))
    else:
        print('')
        for h in player.hands:
            print('     Hand {}: '.format(player.hands.index(h) + 1),end=' ')
            for c in h.cards:
                Print_Card(c)
            print('({}) ${}'.format(h.value, h.bet))

# recursive function for playing through a player's turn
def Play(dealt):
    for hand in player.hands:
        while not hand.bust and not hand.stand:
            Update_Display()
            
            if len(player.hands) == 1:
                move = input(":")
            else:
                move = input("#{}:".format(player.hands.index(hand)+1))

            if move == 's':
                hand.stand = True

            elif move == 'h':
                hand.Add_Card(deck.pop())
                dealt += 1

            elif move == 'd':
                if len(hand.cards) > 2:
                    continue
                hand.Add_Card(deck.pop())
                hand.bet *= 2
                hand.stand = True
                # dealt += 1

            elif move == 'sp':
                if len(player.hands) == 4:
                    continue
                new_hand = Hand()
                new_hand.bet = hand.bet
                new_hand.Add_Card(hand.Remove_Card())
                player.hands.append(new_hand)
                Play(dealt)


if __name__ == '__main__':

    mode = 'menu'
    sub_mode = 'shoe'

    shoe_size = 1
    minimum_bet = 1
    blackjack_payout = 1.5
    hit_soft_17 = False

    deck = [i for j in range(shoe_size) for i in range(DECK_SIZE)]
    random.shuffle(deck)

    dealt = 0

    dealer = Player('Dealer', hand=Hand())
    player = Player('Player', 5000, hand=Hand())


    while True:

        if mode == 'quit':
            #save profile
            print("Goodbye {}.".format(player.name))
            break

        elif mode == 'menu':
            os.system('cls')
            x = input('~~Welcome to CLI Blackjack~~\n(P)lay, (S)ettings, (Q)uit\n:')
            if x is 'p':
                mode = 'play'
            elif x is 's':
                mode = 'settings'
            elif x is 'q':
                mode = 'quit'

        elif mode == 'settings':
            os.system('cls')

            if sub_mode == 'shoe':
                x = input('Shoe Size (1-8): ')
                try:
                    shoe_size = int(x)
                except ValueError:
                    continue
                deck = [i for j in range(shoe_size) for i in range(DECK_SIZE)]
                random.shuffle(deck)
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
                if hit_soft_17 in ['t', 'true', 'y', 'yes']:
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
                mode = 'menu'

        elif mode == 'play': 
            dealer_hand = dealer.hands[0]
            player_hand = player.hands[0]

            x = input('{} ${} Bet: '.format(player.name, player.bank))
            try:
                player_hand.bet = int(x)
            except ValueError:
                if x == 'q':
                    mode = 'quit'
                    continue
                elif x == 'm':
                    mode = 'menu'
                    continue
                elif x == '':
                    player_hand.bet = minimum_bet
                else:
                    continue
            if player_hand.bet < minimum_bet:
                player_hand.bet = minimum_bet


            dealer_hand.cards.append(deck.pop())
            player_hand.cards.append(deck.pop())
            dealer_hand.cards.append(deck.pop())
            player_hand.cards.append(deck.pop())
            dealt += 4

            dealer_hand.Update_Value()
            player_hand.Update_Value()

            if dealer_hand.value == 21 and player_hand.value != 21:
                player.bank -= player_hand.bet
            elif player_hand.value == 21:
                player_hand.bet *= blackjack_payout
            else:
                Play(dealt)

            while dealer_hand.value < 17:
                dealer_hand.cards.append(deck.pop())
                dealer_hand.Update_Value()
                dealt += 1

            for h in player.hands:
                if h.bust or (h.value < dealer_hand.value and not dealer_hand.value > 21):
                    player.bank -= h.bet
                elif h.value == dealer_hand.value:
                    pass
                else:
                    player.bank += h.bet
        
            Update_Display(flip = True)

            player.hands.clear()     
            dealer.hands.clear() 
            dealer.hands.append(Hand()) 
            player.hands.append(Hand())

            if dealt > (DECK_SIZE * shoe_size) * 3/4:
                deck.clear()
                deck = [i for j in range(shoe_size) for i in range(DECK_SIZE)]
                random.shuffle(deck)
                dealt = 0

