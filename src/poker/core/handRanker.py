if not (__name__ == '__main__'):
    from . import core as c
    from . import enums as e
else:
    import core as c
    import enums as e


class HandRanker:
    
    def rank(self,communalCards, hand):
        if not communalCards == None:
            self.cards = communalCards + hand
        else:
            self.cards = hand

        #royal flush
        if self.royalFlush():
            return e.HANDRANK.ROYAL_FLUSH
        #straight flush NEED TO FIX THIS
        elif self.straightFlush():
            return e.HANDRANK.STRAIGHT_FLUSH
        #four of a kind
        elif self.hasPair(4):
            return e.HANDRANK.FOUR_OF_A_KIND
        #full house
        elif self.hasPair(3) and self.hasPair(2):
            return e.HANDRANK.FULL_HOUSE
        #flush
        elif self.flush():
            return e.HANDRANK.FLUSH
        #straight
        elif self.straight():
            return e.HANDRANK.STRAIGHT
        #three of a kind
        elif self.hasPair(3):
            return e.HANDRANK.THREE_OF_A_KIND
        #two pair
        elif self.twoPair():
            return e.HANDRANK.TWO_PAIR
        #pair
        elif self.hasPair(2):
            return e.HANDRANK.PAIR
        #high card
        else:
            return e.HANDRANK.HIGH_CARD
    
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
    
    def flush(self, cardsToCheck = None):
        if cardsToCheck == None:
            cards = self.cards
        else:
            cards = []
            for x in cardsToCheck:
                cards.append(x[0])
        suitMapping = {}
        for card in cards:
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
            cardValues.append((card,int(card.value)))
        cardValues = sorted(cardValues, key=lambda x: x[1])
        
        if len(cardValues) < 5:
            return False

        for i in range(0,3):
            tmpCard = cardValues[i][1]
            counter = 1
            straightCards = [cardValues[i]]
            for j in range(i+1, len(cardValues)):
                if (cardValues[j][1] - tmpCard) == 1:
                    tmpCard = cardValues[j][1]
                    straightCards.append(cardValues[j])
                    counter += 1
                else:
                    break
            if counter == 5:
                self.straightCards = straightCards
                return True
        return False

    def straightFlush(self):
        if self.straight():
            return self.flush(self.straightCards)
    
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
