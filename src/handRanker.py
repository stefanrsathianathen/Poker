
import core as c
import enums as e

class HandRanker:
    def __init__(self,communalCards, hand):
        self.communalCards = communalCards
        self.hand = hand
        self.rank()
    
    def rank(self):
        # merge both arrays
        self.cards = self.communalCards + self.hand

        #royal flush
        if self.royalFlush():
            print("Royal Flush")
        #straight flush
        elif self.straight() and self.flush():
            print("Straight Flush")
        #four of a kind
        elif self.hasPair(4):
            print("Four of a kind")
        #full house
        elif self.hasPair(3) and self.hasPair(2):
            print("Full House")
        #flush
        elif self.flush():
            print("Flush")
        #straight
        elif self.straight():
            print("Straight")
        #three of a kind
        elif self.hasPair(3):
            print("Three of a kind")
        #two pair
        elif self.twoPair():
            print("Two pair")
        #pair
        elif self.hasPair(2):
            print("Pair")
        #high card
        else:
            print("High Card")
    
    def hasPair(self, threshold):
        cardMapping = {}
        for card in self.cards:
            if card.value not in cardMapping:
                cardMapping[card.value] = 0
            cardMapping[card.value] += 1

        for card in cardMapping.keys():
            if cardMapping[card] == threshold:
                return True
        
        return False
    
    def twoPair(self):
        cardMapping = {}
        pair = 0
        for card in self.cards:
            if card.value not in cardMapping:
                cardMapping[card.value] = 0
            cardMapping[card.value] += 1

        for card in cardMapping.keys():
            if cardMapping[card] == 2:
                pair += 1
        
        if pair == 2:
            return True
        return False
    
    def flush(self):
        suitMapping = {}
        for card in self.cards:
            if card.suit[1] not in suitMapping:
                suitMapping[card.suit[1]] = 0
            suitMapping[card.suit[1]] += 1
        
        for suit in suitMapping.keys():
            if suitMapping[suit] >= 5:
                return True
        return False

    def straight(self):
        cardValues = []
        for card in self.cards:
            cardValues.append(card.value)
        cardValues = sorted(cardValues)
        
        for i in range(0,3):
            tmpCard = cardValues[i]
            counter = 1
            for j in range(i+1, len(cardValues)):
                if (cardValues[j] - tmpCard) == 1:
                    tmpCard = cardValues[j]
                    counter += 1
                else:
                    break
            if counter == 5:
                return True
        return False
    
    def royalFlush(self):
        cardValues = []
        for card in self.cards:
            cardValues.append(card.value)
        cardValues = sorted(cardValues)

        for x in [10, 11, 12, 13, 1]:
            if x in cardValues:
                continue
            else:
                return False
        return self.flush()