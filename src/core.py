class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
    
    def show(self):
        if self.value == 1:
            trueValue = "Ace"
        elif self.value == 11:
            trueValue = "Jack"
        elif self.value == 12:
            trueValue = "Queen"
        elif self.value == 13:
            trueValue = "King"
        else:
            trueValue = str(self.value)
        print("{} of {}".format(trueValue, self.suit[0]))

    def __str__(self):
        if self.value == 1:
            trueValue = "A"
        elif self.value == 11:
            trueValue = "J"
        elif self.value == 12:
            trueValue = "Q"
        elif self.value == 13:
            trueValue = "K"
        else:
            trueValue = str(self.value)
        return f"{trueValue}{self.suit[0]}"

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in [("♠","s"), ("♣","c"), ("♦","d"), ("♥","h")]:
            for v in range(1, 14):
                self.cards.append(Card(s, v))
    
    def show(self):
        for c in self.cards:
            c.show()

    def shuffle(self):
        import random
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]
    
    def drawCard(self):
        return self.cards.pop()
    
class Player:
    def __init__(self, name, stackSize):
        self.name = name
        self.stack = stackSize
    
    def action(self,round):
        pass

    def draw(self, deck):
        self.hand = Hand(deck)
    
    def showHand(self):
        return str(self.hand)
    
    def cards(self):
        return self.hand.cards()

    def reset(self):
        self.hand = []
    
    def getName(self):
        return self.name

    def bet(self, amount):
        self.stack -= amount
    
    def validBet(self, amount):
        return self.stack - amount  >= 0

    def getStack(self):
        return self.stack

class Hand:
    def __init__(self,deck):
        self.deck = deck
        self.draw()

    def draw(self):
        self.first = self.deck.drawCard()
        self.second = self.deck.drawCard()
        
        #this will be used for ai players
        if self.first.suit == self.second.suit:
            self.suited = True
        else:
            self.suited = False
    
    def cards(self):
        return [self.first, self.second]

    def __str__(self):
        return f"({self.first},{self.second})"