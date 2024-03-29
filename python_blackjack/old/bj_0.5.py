import random
import sys
import os

DECK_SIZE = 52

class Hand():
   def __init__(self):
      self.cards = []
      self.value = 0
      self.bet = 0
      self.last_bet = 0
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

# Player.cards is an 2d array of cards, the first dimension is for each split hand. THe second dimension are the cards themselves.
class Player():
   def __init__(self, name = '', bank = '', hand = Hand()):
      self.name = name
      self.bank = bank
      self.hand = []
      self.hand.append(hand)
      self.hand_index = 1

def Print_Card(card):
   suite = card//13
   value = card%13+1
   if suite == 0:
      print('C',end='')
   elif suite == 1:
      print('D',end='')
   elif suite == 2:
      print('H',end='')
   elif suite == 3:
      print('S',end='')
   if value == 1:
      print('A',end='')
   elif value == 11:
      print('J',end='')
   elif value == 12:
      print('Q',end='')
   elif value == 13:
      print('K',end='')
   else:
      print(value,end='')
   print('',end=' ')

def Show(flip = False):
   os.system('cls')
   print('Dealer:',end=' ')
   if not flip:
         print('X',end=' ')
         Print_Card(dealer_hand.cards[len(dealer_hand.cards)-1])
         print('')
   else:
      for c in dealer_hand.cards:
            Print_Card(c)
      print('({})'.format(dealer_hand.value))

   print('Player:',end=' ')
   if len(player.hand) == 1:
      for c in player.hand[0].cards:
         Print_Card(c)
      print('({}) ${}'.format(player.hand[0].value, player.hand[0].bet))
   else:
      print('')
      for h in player.hand:
         print('    Hand {}: '.format(player.hand.index(h) + 1),end=' ')
         for c in h.cards:
            Print_Card(c)
         print('({}) ${}'.format(h.value, h.bet))
   Show_Count()

def Show_Count():
   print(true_count)

def Get_Input(mode = ''):
   x = ''

   if mode is 'bet':
      x = input('Player Bank: ${} Place Bet: '.format(player.bank))
      if x is 'q':
         sys.exit()
      elif x is '':
         player.hand[0].bet = player.hand[0].last_bet
      elif x.isdigit():
         player.hand[0].last_bet = int(x)
         return int(x)
      else:
         return Get_Input('bet')

   if mode is 'play':
      if len(player.hand) != 1:
         x = input('#{}:'.format(player.hand_index))
      else:
         x = input(':')
      if x == 'q':
         sys.exit()
      elif x.isalpha():
         return x.lower()
      else:
         return Get_Input('play')

   if mode is 'settings':
      pass

# player_cards are a list of hands generated by dealing and then splitting hands.
def Play(deck, player_cards):
   # cycle through hands made by split
   for hand in player_cards:
      player.hand_index = player_cards.index(hand)
      # keep hitting until stand or bust
      while not hand.bust and not hand.stand:
         # update display with new cards and/or bet
         Show()
         # show input for particular split hand
         x = Get_Input('play')
         if x == 's':
            hand.stand = True
            break
         elif x == 'h':
            hand.cards.append(deck.pop())
            hand.Update_Value()
            if hand.value > 21:
               hand.bust = True
            continue
         elif x == 'd':
            if len(hand.cards) > 2:
               print('cannot double after hit')
               continue
            hand.cards.append(deck.pop())
            hand.Update_Value()
            if hand.value > 21:
               hand.bust = True
            hand.bet *= 2
            hand.stand = True
            break
         elif x == 'sp':
            if len(player_cards) == 4:
               print('cannot split again')
               continue
            new_hand = Hand()
            new_hand.bet = hand.bet
            new_hand.cards.append(hand.cards.pop())
            hand.Update_Value()
            new_hand.Update_Value()
            player_cards.append(new_hand)
            Play(deck, player_cards)
            break

def Count(card):
   played_cards.append(card)
   count = 0
   for c in played_cards:
      if c.value < 7:
         count -= 1
      elif c.value > 8:
         count += 1
   return count*(played_cards/deck_size)

deck = []
for i in range(DECK_SIZE):
   deck.append(i)
random.shuffle(deck)
played_cards = []
shoe_size = 1
deck_size = shoe_size * DECK_SIZE
true_count = 0

dealer = Player('Dealer', 1000000)
dealer_hand = dealer.hand[0]

hand = Hand()
player = Player('Player', 5000, hand)

os.system('cls')
while True:
   player_hand = player.hand[0]
   player_hand.bet = Get_Input('bet')
   if player_hand.bet == 'q':
      sys.exit()

   dealer_hand.cards.append(deck.pop())
   player_hand.cards.append(deck.pop())
   dealer_hand.cards.append(deck.pop())
   player_hand.cards.append(deck.pop())

   dealer_hand.Update_Value()
   player_hand.Update_Value()

   if dealer_hand.value == 21 and player_hand.value != 21:
      player.bank -= player_hand.bet
   elif player_hand.value == 21:
      player_hand.bet *= 1.5
   else:
      Play(deck, player.hand)

   while dealer_hand.value < 17:
      dealer_hand.cards.append(deck.pop())
      dealer_hand.Update_Value()

   for h in player.hand:
      if h.bust or (h.value < dealer_hand.value and not dealer_hand.value > 21):
         player.bank -= h.bet
      elif h.value == dealer_hand.value:
         pass
      else:
         player.bank += h.bet
 
   Show(flip = True)

   player.hand.clear()
   player.hand.append(Hand())      
   dealer_hand.cards.clear()
   dealer_hand.value = 0   
   
