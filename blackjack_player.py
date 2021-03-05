class player(object):
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.bust = False
        self.stand = False
        self.balance = 100

    def reset(self):
        self.hand = []
        self.bust = False
        self.stand = False
        #self.balance = 100

    def hit(self,card):
        if not self.stand:
           self.hand.append(card)

    def busted(self):
        self.bust = True
        self.stand = True

    def stood(self):
        self.stand = True

    def score(self):
        sc = 0
        A = 0
        for num in self.hand:
            if num[1:] == 'A':
                A += 1
            elif num[1:] =='J' or num[1:] == 'Q' or num[1:] == 'K':
                sc += 10
            else:
                sc += int(num[1:])
        if A == 0:
            if sc > 21:
                self.busted()
            elif sc == 21:
                self.stood()
            return sc
        res = [sc]

        for i in range (A):
            temp = []
            for item in res:
                temp.append(item+1)
                temp.append(item+11)
            res = temp
        if min(res) > 21:
            self.busted()
            return min(res)

        else:
            maxx = max([x for x in res if x <= 21])
            if maxx == 21:
                self.stood()
            return max([x for x in res if x <= 21])


    def print_result(self):
        res = self.name + ' $'+str(self.balance)
        res += '\n' + ','.join(self.hand)
        res += '\nscore:' + str(self.score())
        return res

"""
a = player('a','b')
a.hit('♦A')
a.hit('♦10')
print (a.print_result())
"""