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
        print("{} of {}".format(trueValue, self.suit))

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ["♠", "♣", "♦", "♥"]:
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
    def __init__(self, name):
        self.name = name
    
    def draw(self, deck):
        self.hand = Hand(deck)
    
    def showHand(self):
        self.hand.showHand()

    def reset(self):
        self.hand = []
    
    def getName(self):
        return self.name

class Hand:
    def __init__(self,deck):
        self.deck = deck
        self.hand = []
        self.draw()

    def draw(self):
        self.hand.append(self.deck.drawCard())
        self.hand.append(self.deck.drawCard())

    def showHand(self):
        for card in self.hand:
            card.show()