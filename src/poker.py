import core as c

class PokerPlayer(c.Player):
    def __init__(self, name):
        super().__init__(name)
        #this should not be hardcoded
        stack = 100


class Poker:
    def __init__(self):
        self.roundNumber = 1
        #this is hardcoded
        self.players = [PokerPlayer("1"), PokerPlayer("2")]

    def playRound(self):
        self.round = Round(self.players)
        self.roundNumber += 1

class Round:
    def __init__(self, players):
        self.newDeck()
        self.players = players

    def newDeck(self):
        self.deck = c.Deck()
        self.deck.shuffle()

    def deal(self):
        for player in self.players:
            player.draw(self.deck)

    def flop(self):
        #burn a card
        self.deck.drawCard()

        self.communalCards = [self.deck.drawCard() for i in range(3)]
        print("The flop is: ")
        self.showCommunalCards()
        print("\n")

    def turn(self):
        self.communalCards.append(self.deck.drawCard())
        print("After turn card:")
        self.showCommunalCards()

    def river(self):
        self.communalCards.append(self.deck.drawCard())
        print("After river card:")
        self.showCommunalCards()

    def showCommunalCards(self):
        for card in self.communalCards:
            card.show()
        print("\n")

    def showAllHands(self):
        for player in self.players:
            print(player.getName() + "'s hand: ")
            player.showHand()
            print("\n")


# this is all testing driver code (will change)
game = Poker()
game.playRound()
game.round.deal()

game.round.flop()
game.round.turn()
game.round.river()

game.round.showAllHands()