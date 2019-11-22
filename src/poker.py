import core as c
from enum import Enum,auto

class PokerPlayer(c.Player):
    def __init__(self, name):
        super().__init__(name)
        #this should not be hardcoded
        stack = 100
    
    def action(self):
        pass

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
        self.status = STATUS.IN_ROUND
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
        while self.status == STATUS.IN_ROUND:
            self.players[playerPointer].action()
            playerPointer += 1
            if playerPointer == self.amountOfPlayers:
                self.dealCommunalCards()
                playerPointer = 0


    def dealCommunalCards(self):
        if self.dealRound == 3:
            #burn a card
            self.deck.drawCard()
            self.communalCards = [self.deck.drawCard() for i in range(3)]
            print("After the flop: ")
            self.showCommunalCards()
            self.dealRound = 2
        
        elif self.dealRound == 2:
            self.communalCards.append(self.deck.drawCard())
            print("After the turn: ")
            self.showCommunalCards()
            self.dealRound = 1
        
        elif self.dealRound == 1:
            self.communalCards.append(self.deck.drawCard())
            print("After the river: ")
            self.showCommunalCards()
            self.dealRound = 0
        
        else:
            self.status = STATUS.FINISH
            self.showAllHands() #this will find winners or something

    def showCommunalCards(self):
        for card in self.communalCards:
            card.show()
        print("\n")

    def showAllHands(self):
        for player in self.players:
            print(player.getName() + "'s hand: " + player.showHand())
            print("\n")


class ACTION(Enum):
    BET = auto()
    CALL = auto()
    FOLD = auto()

class STATUS(Enum):
    IN_ROUND = auto()
    FINISH = auto()

# this is all testing driver code (will change)
game = Poker()
game.playRound()