import unittest
import context
from poker import core

class TestCore(unittest.TestCase):

    def test_card(self):
        card = core.Card(("♠","s"), 1)
        self.assertEqual(card.value, 1)
        self.assertEqual(card.suit, ("♠","s"))

    def test_deck_length(self):
        deck = core.Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_take_one_card(self):
        deck = core.Deck()
        deck.drawCard()
        self.assertEqual(len(deck.cards), 51)
        deck.drawCard()
        self.assertEqual(len(deck.cards), 50)

    def test_create_player(self):
        player = core.Player("Bob", 100)
        self.assertEqual(player.getName(), "Bob")
        self.assertEqual(player.getStack(), 100)
        self.assertEqual(player.getHand(), [])
    
    def test_draw_cards(self):
        deck = core.Deck()
        player = core.Player("Bob", 100)
        player.draw(deck)
        self.assertEqual(len(deck.cards), 50)
        self.assertEqual(len(player.hand.cards()), 2)
        

if __name__ == 'main':
    unittest.main()