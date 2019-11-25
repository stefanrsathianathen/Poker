import core as c
import enums as e
import handRanker as ranker

class PokerPlayer(c.Player):
    def __init__(self, name):
        super().__init__(name, 100)
        #this should not be hardcoded

    
    def action(self, roundDetails):
        self.handRank = ranker.HandRanker().rank(roundDetails.getCommunalCards(), self.cards())
        print("The Communal cards: ")
        roundDetails.showCommunalCards()
        print("Your Hand: " + self.showHand())
        print("What do you want to do?")
        decision = input()
        return self.handleDecision(decision, roundDetails)

    def isValidAmount(self, amount):
        if (self.stack - amount) >= 0:
            return True
        return False

    def handleDecision(self, usersInput, roundDetails):
        userDecision = usersInput.lower().split()
        move = userDecision[0]
        if move == 'c' or move == 'call':
            return { "action": e.ACTION.CALL }
        elif move == 'b' or move == 'bet':
            return { "action": e.ACTION.BET, "amount": int(userDecision[1])}
        elif move == 'f' or move == 'fold':
            return { "action": e.ACTION.FOLD}
        elif move == 'a' or move == 'allin' or move == 'all':
            return { "action": e.ACTION.ALLIN}


class Poker:
    def __init__(self):
        self.roundNumber = 1
        #this is hardcoded
        self.smallBlind = 5
        self.bigBlind = 10
        self.players = [PokerPlayer("Tom"), PokerPlayer("Gina")]
        self.smallBlindPlayer = 0 #use index
        self.bigBlindPlayer = 1 #use index
        print("Here is how to enter your decision")
        print("Call or C")
        print("Bet Amount or B Amount")
        print("Fold or F")
        print("Allin or A")
        print("\n")

    def playRound(self):
        self.round = Round(self.players,self.bigBlind)
        self.roundNumber += 1

class Round:
    def __init__(self, players,bigBlind):
        self.newDeck()
        self.__players = players
        self.amountOfPlayers = len(self.__players)
        self.dealRound = 3
        self.pot = 0
        self.amountToCall = bigBlind
        self.__playersCurrentBets = [0]*len(players)
        self.__status = e.ROUNDSTATUS.IN_ROUND
        self.__bettingStatus = e.BETTINGSTATUS.BETTING
        self.communalCards = None
        self.play()

    def newDeck(self):
        self.deck = c.Deck()
        self.deck.shuffle()

    def deal(self):
        for player in self.__players:
            player.draw(self.deck)

    def play(self):
        self.deal()
        playerPointer = 0
        while self.__status == e.ROUNDSTATUS.IN_ROUND:
            action = self.__players[playerPointer].action(self)
            self.processPlayerAction(action, playerPointer)
            playerPointer += 1

            if self.amountOfPlayers == 1:
                self.printWinner()
                self.__status = e.ROUNDSTATUS.FINISH

            elif playerPointer == self.amountOfPlayers:
                if self.__bettingStatus == e.BETTINGSTATUS.READY:
                    self.dealCommunalCards()
                playerPointer = 0

    def processPlayerAction(self, action, player):
        playerMove = action["action"]
        if playerMove == e.ACTION.FOLD:
            self.amountOfPlayers -= 1
            self.__playersCurrentBets[player] = None
        # if this is the last play make check to see if ready to move on
        elif (player + 1) == self.amountOfPlayers and self.isReadyForCommunalCards():
            self.__bettingStatus = e.BETTINGSTATUS.READY

    def isReadyForCommunalCards(self):
        bets = set(self.__playersCurrentBets)
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
            self.__status = e.ROUNDSTATUS.FINISH
            self.showAllHands() #this will find winners or something

    def __showCards__(self):
        self.showCommunalCards()
        self.bettingStatus = e.BETTINGSTATUS.BETTING
        self.__playersCurrentBets = [0 if x != None else None for x in self.__playersCurrentBets]
        self.dealRound -= 1

    def showCommunalCards(self):
        if self.communalCards == None:
            print("No communal cards yet\n")
        else:
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
        self.printWinner()
        for player in self.__players:
            print(player.getName() + "'s hand: " + player.showHand() + " " + player.handRank.value[1])
            print("\n")

    def printWinner(self):
        # if there is only one player left they are winner by default, otherwise find people with strongest hand. (Need to implement better hand comparison)
        if self.amountOfPlayers == 1:
            player = -1
            for x in range(0, len(self.__playersCurrentBets)):
                if self.__playersCurrentBets != None:
                    player = x
                    break
            print(self.__players[x].getName() + " win's")
            return
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


    def findWinner(self):
        player = None
        hand = e.HANDRANK.NOTHING
        for p in self.__players:
            if p.handRank > hand:
                player = [p]
                hand = p.handRank
            elif p.handRank == hand:
                player.append(p)
        return (player, hand)


# this is all testing driver code (will change)
game = Poker()
game.playRound()