
from random import shuffle

deck = []
dealer = []
dealer_value = 0
player = []
player_current_hand = 0
player_bet = []
player_value = []
player_bank = 5000

table_min = 10
table_shoe = 6
table_soft = False

deck = [i for j in range(table_shoe) for i in range(52)]

while True:
    player_bet.append(table_min)
    dealer.append(deck.pop())
    player.append(deck.pop())
    dealer.append(deck.pop())
    player.append(deck.pop())
    dealer_ace = 0
    for c in dealer:
        if c%13+1 == 1:
            dealer_value += 11
            dealer_ace += 1
        else:
            dealer_value += min(c%13+1, 10)
        if dealer_value > 21 and dealer_ace > 0:
            dealer_value -= 10
            dealer_ace -= 1
    val = 0
    ace = 0
    for c in player:
        if c%13+1 == 1:
            val += 11
            ace += 1
        else:
            val += min(c%13+1, 10)
        if val > 21 and ace > 0:
            val -= 10
            ace -= 1
    player_value.append(val)

    if dealer_value != 21 and player_value != 21:
        while player_current_hand > 0:
        while player_value[0] <= 21:
            x = input(":")
            if x == 'hit':
                player.append(deck.pop())
            elif x == 'stay':
                break
            elif x == 'double':
                player_bet *= 2
                player.append(deck.pop())
                break
            elif x == 'split':
                tmp = player
                player.clear()
                player_value.clear()
                player.append([])
                player.append([])
                player[1].append(tmp.pop())
                player[2].append(tmp.pop())
                for h in player:
                    ace = 0
                    val = 0
                    while val <= 21:
                        x = input(":")
                        if x == 'hit':
                            player.append(deck.pop())
                        elif x == 'stay':
                            break
                        elif x == 'double':
                            player_bet *= 2
                            player.append(deck.pop())
                            break
                        elif x == 'split':
                            player.append(h.pop())
                        for c in h:
                            if c%13+1 == 1:
                                val += 11
                                ace += 1
                            else:
                                val += c%13+1
                            if val > 21 and ace > 0:
                                val -= 10
                                ace -= 1
                    player_value.append(val)
            break

                                                                               