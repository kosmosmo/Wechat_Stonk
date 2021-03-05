import blackjack_player,random
class game(object):
    def __init__(self,players):
        cards = ['A' ,'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['♣','♦','♥','♠']
        self.deck = []
        for card in cards:
            for suit in suits:
                self.deck.append(suit+card)
        self.players = players
        self.start = False
        self.move = {}
        self.orders = []
        self.dealer = 0
        self.balance = {}

    def add_move(self,player,move):
        self.move[player] = move

    def new_game(self):
        for key,val in self.players.items():
            val.reset()
        self.start = False
        self.move = {}
        self.dealer += 1
        self.dealer = self.dealer % len(self.players)
        self.balance = {}

    def deal(self):
        scores = []
        self.start = True
        for key,val in self.players.items():
            self.balance[key] = 0
            self.add_move(key,'')
            self.orders.append(key)
            for i in range(2):
                random.shuffle(self.deck)
                card = self.deck.pop()
                val.hit(card)
            sc = val.score()
            if sc == 21: self.add_move(key,'s')
            val_res = ''
            if key == self.orders[self.dealer]:
                val_res += 'D* '
            val_res += val.print_result()
            scores.append(val_res)
        return scores

    def next(self):
        scores = []
        for key,val in self.move.items():
            if val == 'h' and self.players[key].stand != True:
                random.shuffle(self.deck)
                card = self.deck.pop()
                self.players[key].hit(card)
            elif val == 's':
                self.players[key].stood()
            self.players[key].score()
            val_res = ''
            if key == self.orders[self.dealer]:
                val_res += 'D* '
            val_res += self.players[key].print_result()
            scores.append(val_res)
        return scores

    def check_move(self):
        ct = 0
        for key, val in self.move.items():
            if val != '':
                ct += 1
        return ct


    def check_winner(self):
        ct = 0
        for key, val in self.players.items():
            #print (key,val.stand)
            if val.stand == True:
                ct += 1
        if ct == len(self.players):
            dealer_name = self.orders[self.dealer]
            dealer_score = self.players[dealer_name].score()
            dealer_busted = self.players[dealer_name].bust
            if dealer_busted:
                for key,val in self.players.items():
                    if key == dealer_name: continue
                    self.players[dealer_name].balance -=1
                    self.balance[dealer_name] -=1
                    if key != dealer_name:
                        self.players[key].balance += 1
                        self.balance[key] += 1
            else:
                for key, val in self.players.items():
                    if key == dealer_name: continue
                    player_score = self.players[key].score()
                    if player_score <= 21 and player_score > dealer_score:
                        self.players[dealer_name].balance -= 1
                        self.balance[dealer_name] -= 1
                        self.players[key].balance += 1
                        self.balance[key] += 1
                    else:
                        self.players[dealer_name].balance += 1
                        self.balance[dealer_name] += 1
                        self.players[key].balance -= 1
                        self.balance[key] -= 1
            return True

        else:
            return False

"""
players = {'player01':blackjack_player.player('player01'),
           'player02':blackjack_player.player('player02'),
           'player03':blackjack_player.player('player03')}

commands01 = {'player01':'h',
           'player02':'h',
           'player03':'h'}
commands02 = {'player01':'h',
           'player02':'h',
           'player03':'s'}
commands03 = {'player01':'h',
           'player02':'h',
           'player03':'s'}
a = game(players)
print (a.deal())
a.move = commands01
print (a.next())
print (a.check_winner())

a.move = commands02
print (a.next())
print (a.check_winner())
print (a.balance)

a.move = commands03
print (a.next())
print (a.check_winner())
print (a.balance)
"""