import core as c
import enums as e
import handRanker as ranker

class PokerPlayer(c.Player):
    def __init__(self, name):
        super().__init__(name)
        #this should not be hardcoded
        stack = 100

    
    def action(self, roundDetails):
        self.handRank = ranker.HandRanker().rank(roundDetails.getCommunalCards(), self.cards())
        # print("The Communal cards: ")
        # roundDetails.getCommunalCards()
        # print("The current bet is: " + str(roundDetails.amountToCall))
        # print("Your Cards:" + self.showHand())
        


class Poker:
    def __init__(self):
        self.roundNumber = 1
        #this is hardcoded
        self.smallBlind = 5
        self.bigBlind = 10
        self.players = [PokerPlayer("Tom"), PokerPlayer("Luke"), PokerPlayer("Gina")]
        self.smallBlindPlayer = 0 #use index
        self.bigBlindPlayer = 1 #use index

    def playRound(self):
        self.round = Round(self.players,self.bigBlind)
        self.roundNumber += 1

class Round:
    def __init__(self, players,bigBlind):
        self.newDeck()
        self.players = players
        self.amountOfPlayers = len(self.players)
        self.dealRound = 3
        self.pot = 0
        self.amountToCall = bigBlind
        self.playersCurrentBets = [0]*len(players)
        self.status = e.ROUNDSTATUS.IN_ROUND
        self.bettingStatus = e.BETTINGSTATUS.BETTING
        self.communalCards = None
        self.play()

    def newDeck(self):
        self.deck = c.Deck()
        self.deck.shuffle()

    def deal(self):
        for player in self.players:
            player.draw(self.deck)

    def play(self):
        self.deal()
        playerPointer = 0
        while self.status == e.ROUNDSTATUS.IN_ROUND:
            action = self.players[playerPointer].action(self)
            self.processPlayerAction(action, playerPointer)
            playerPointer += 1
            if playerPointer == self.amountOfPlayers:
                if self.bettingStatus == e.BETTINGSTATUS.READY:
                    self.dealCommunalCards()
                playerPointer = 0

    def processPlayerAction(self,action, player):
        # if this is the last play make check to see if ready to move on
        if (player + 1) == self.amountOfPlayers and self.isReadyForCommunalCards():
            self.bettingStatus = e.BETTINGSTATUS.READY

    def isReadyForCommunalCards(self):
        bets = set(self.playersCurrentBets)
        return len(bets) == 1 or (len(bets) == 2 and (None in bets))

    def dealCommunalCards(self):
        if self.dealRound == 3:
            #burn a card
            self.deck.drawCard()
            self.communalCards = [self.deck.drawCard() for i in range(3)]
            print("After the flop: ")
            self.__showCards__()
        
        elif self.dealRound == 2:
            self.communalCards.append(self.deck.drawCard())
            print("After the turn: ")
            self.__showCards__()
        
        elif self.dealRound == 1:
            self.communalCards.append(self.deck.drawCard())
            print("After the river: ")
            self.__showCards__()
        
        else:
            self.status = e.ROUNDSTATUS.FINISH
            self.showAllHands() #this will find winners or something

    def __showCards__(self):
        self.showCommunalCards()
        self.bettingStatus = e.BETTINGSTATUS.BETTING
        self.dealRound -= 1

    def showCommunalCards(self):
        for card in self.communalCards:
            card.show()
        print("\n")

    def getCommunalCards(self):
        if self.communalCards == None:
            return []
        else:
            return self.communalCards

    def showAllHands(self):
        print("Communal Cards:")
        self.showCommunalCards()
        winners = self.findWinner()
        if len(winners[0]) == 1:
            print(winners[0][0].getName() + " win's with a " + winners[1].value[1])
            print("\n")
        else:
            winnersStr = ""
            for x in range(0, len(winners)):
                winnersStr += winners[0][x].getName()
                if x < len(winners) - 1:
                    winnersStr += ", "
            winnersStr += " split pot with a " + winners[1].value[1]
            print(winnersStr + "\n")

        for player in self.players:
            print(player.getName() + "'s hand: " + player.showHand() + " " + player.handRank.value[1])
            print("\n")

    def findWinner(self):
        player = None
        hand = e.HANDRANK.NOTHING
        for p in self.players:
            if p.handRank > hand:
                player = [p]
                hand = p.handRank
            elif p.handRank == hand:
                player.append(p)
        return (player, hand)


# this is all testing driver code (will change)
game = Poker()
game.playRound()