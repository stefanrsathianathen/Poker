import core as c
import enums as e
import handRanker as ranker

class PokerPlayer(c.Player):
    def __init__(self, name):
        super().__init__(name)
        #this should not be hardcoded
        stack = 100

    
    def action(self, roundDetails):
        pass
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
            self.showCommunalCards()
            self.bettingStatus = e.BETTINGSTATUS.BETTING
            self.dealRound = 2
        
        elif self.dealRound == 2:
            self.communalCards.append(self.deck.drawCard())
            print("After the turn: ")
            self.showCommunalCards()
            self.bettingStatus = e.BETTINGSTATUS.BETTING
            self.dealRound = 1
        
        elif self.dealRound == 1:
            self.communalCards.append(self.deck.drawCard())
            print("After the river: ")
            self.showCommunalCards()
            self.bettingStatus = e.BETTINGSTATUS.BETTING
            self.dealRound = 0
        
        else:
            self.status = e.ROUNDSTATUS.FINISH
            self.showAllHands() #this will find winners or something

    def showCommunalCards(self):
        for card in self.communalCards:
            card.show()
        print("\n")

    def getCommunalCards(self):
        if self.communalCards == None:
            return ""
        else:
            self.showCommunalCards()

    def showAllHands(self):
        print("\n\nCommunal Cards")
        # print the winner
        self.showCommunalCards()
        for player in self.players:
            print(player.getName() + "'s hand: " + player.showHand())
            ranker.HandRanker(self.communalCards,player.cards())
            print("\n")

# this is all testing driver code (will change)
game = Poker()
game.playRound()