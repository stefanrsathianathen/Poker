import os
import core as c
import enums as e
import handRanker as ranker

class PokerPlayer(c.Player):
    def __init__(self, name):
        super().__init__(name, 100)
        #this should not be hardcoded

    
    def action(self, roundDetails, limit):
        self.handRank = ranker.HandRanker().rank(roundDetails.getCommunalCards(), self.cards())
        return self.getAction(roundDetails,limit)
        

    def getAction(self, roundDetails, limit):
        self.availableActions(roundDetails, limit)
        action = input()
        internalAction = self.handleAction(action, limit)
        if internalAction == e.ACTION.INVALID:
            return self.getAction(roundDetails, limit)
        return internalAction

    def isValidAmount(self, amount):
        if (self.getStack() - amount) >= 0:
            return True
        return False

    def tableInfo(self, roundDetails):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("The Communal cards: ")
        roundDetails.showCommunalCards()
        print("Pot: " + str(roundDetails.pot))
        print("Your Stack: " + str(self.getStack()))
        print("Your Hand: " + self.showHand())
        print("Currently have: " + str(self.handRank) + "\n")

    def availableActions(self, roundDetails ,limit):
        self.tableInfo(roundDetails)
        print("What do you want to do?")
        print("Call or C")
        if not limit:
            print("Check or CK")
            print("Bet Amount or B Amount")
        elif limit:
            print("Raise Amount or R Amount")
        print("Allin or A")
        print("Fold or F")
        print("\n")

    def handleAction(self, usersInput, limit):
        userAction = usersInput.lower().split()
        move = userAction[0]
        if limit:
            if move == 'ck' or move == 'check' or move == 'b' or move == 'bet':
                return e.ACTION.INVALID
        if move == 'c' or move == 'call':
            return { "action": e.ACTION.CALL }
        elif move == 'b' or move == 'bet':
            return { "action": e.ACTION.BET, "amount": int(userAction[1])}
        elif move == 'f' or move == 'fold':
            return { "action": e.ACTION.FOLD}
        elif move == 'a' or move == 'allin' or move == 'all':
            return { "action": e.ACTION.ALLIN}
        elif move == 'ck' or move == 'check':
            return { "action": e.ACTION.CHECK}
        else:
            return e.ACTION.INVALID


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
        print("Check or CK")
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
            action = self.__players[playerPointer].action(self, self.__limit__(playerPointer))
            self.processPlayerAction(action, playerPointer)
            playerPointer += 1

            if self.amountOfPlayers == 1:
                self.printWinner()
                self.__status = e.ROUNDSTATUS.FINISH

            elif playerPointer == self.amountOfPlayers:
                if self.__bettingStatus == e.BETTINGSTATUS.DONE:
                    self.dealCommunalCards()
                    # reset bets
                playerPointer = 0

    def __limit__(self, playerPointer):
        biggestBet = max(self.__playersCurrentBets)
        return not (self.__playersCurrentBets[playerPointer] == biggestBet)

    def processPlayerAction(self, action, playerIndex):
        playerMove = action["action"]
        player = self.__players[playerIndex]
        if playerMove == e.ACTION.FOLD:
            self.amountOfPlayers -= 1
            self.__playersCurrentBets[playerIndex] = None
        elif playerMove == e.ACTION.BET:
            if (player.validBet(action["amount"])):
                self.__makeBet__(playerIndex, player, action["amount"])
        elif playerMove == e.ACTION.CALL:
            currentBet = self.__playersCurrentBets[playerIndex]
            betAmount = max(self.__playersCurrentBets) - currentBet
            # if a player can call the bet just call
            # otherwise the player should be all in
            if player.validBet(betAmount):
                self.__makeBet__(playerIndex, player, betAmount)
            else:
                self.__makeBet__(playerIndex, player, player.getStack())
        elif playerMove == e.ACTION.ALLIN:
            self.__makeBet__(playerIndex, player, player.getStack())
        elif playerMove == e.ACTION.CHECK:
            pass
        else:
            raise Exception("Unknown state")
        # if this is the last play make check to see if ready to move on
        if (playerIndex + 1) == self.amountOfPlayers and self.isReadyForCommunalCards():
            self.__bettingStatus = e.BETTINGSTATUS.DONE

    def __makeBet__(self, playerIndex, player, amount):
        self.__playersCurrentBets[playerIndex] += amount
        self.pot += amount
        player.bet(amount)

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
        self.__bettingStatus = e.BETTINGSTATUS.BETTING
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
            print(player.getName() + "'s hand: " + player.showHand() + " " + str(player.handRank))
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
            print(winners[0][0].getName() + " win's with a " + str(winners[1]))
            print("\n")
        else:
            winnersStr = ""
            for x in range(0, len(winners)):
                winnersStr += winners[0][x].getName()
                if x < len(winners) - 1:
                    winnersStr += ", "
            winnersStr += " split pot with a " + str(winners[1])
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