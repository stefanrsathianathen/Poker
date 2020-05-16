import unittest
import context

from core import handRanker
from core import core as c
from core import enums as e

class TestCore(unittest.TestCase):
    def setUp(self):
        self.ranker = handRanker.HandRanker()

    def test_high_card(self):
        hand = [c.Card(("♣","c"), 13), c.Card(("♣","c"), 2) ]
        self.assertEqual( self.ranker.rank(None, hand), e.HANDRANK.HIGH_CARD)

    def test_pair(self):
        hand = [c.Card(("♣","c"), 13), c.Card(("♠","s"), 13) ]
        self.assertEqual( self.ranker.rank(None, hand), e.HANDRANK.PAIR)

    def test_two_pair(self):
        communityCards = [c.Card(("♣","c"), 2), c.Card(("♠","s"), 3), c.Card(("♠","s"), 2) ]
        hand = [c.Card(("♣","c"), 13), c.Card(("♠","s"), 13)]
        self.assertEqual(self.ranker.rank(communityCards, hand), e.HANDRANK.TWO_PAIR)
    
    def test_three_of_a_kind(self):
        communityCards = [c.Card(("♣","c"), 2), c.Card(("♠","s"), 3), c.Card(("♠","s"), 6), c.Card(("♥","h"), 13) ]
        hand = [c.Card(("♣","c"), 13), c.Card(("♠","s"), 13)]
        self.assertEqual(self.ranker.rank(communityCards, hand), e.HANDRANK.THREE_OF_A_KIND)
    
    def test_straight(self):
        communityCards = [c.Card(("♣","c"), 2), c.Card(("♠","s"), 3), c.Card(("♠","s"), 6), c.Card(("♥","h"), 8) ]
        hand = [c.Card(("♣","c"), 4), c.Card(("♠","s"), 5)]
        self.assertEqual(self.ranker.rank(communityCards, hand), e.HANDRANK.STRAIGHT)
    
    def test_flush(self):
        communityCards = [c.Card(("♣","c"), 2), c.Card(("♠","s"), 3), c.Card(("♠","s"), 6), c.Card(("♠","s"), 8) ]
        hand = [c.Card(("♠","s"), 4), c.Card(("♠","s"), 5)]
        self.assertEqual(self.ranker.rank(communityCards, hand), e.HANDRANK.FLUSH)
    
    def test_full_house(self):
        communityCards = [c.Card(("♣","c"), 2), c.Card(("♦","d"), 3), c.Card(("♠","s"), 3), c.Card(("♠","s"), 4) ]
        hand = [c.Card(("♠","s"), 4), c.Card(("♥","h"), 3)]
        self.assertEqual(self.ranker.rank(communityCards, hand), e.HANDRANK.FULL_HOUSE)

    def test_four_of_a_kind(self):
        communityCards = [c.Card(("♣","c"), 2), c.Card(("♦","d"), 3), c.Card(("♠","s"), 3), c.Card(("♣","c"), 3) ]
        hand = [c.Card(("♠","s"), 4), c.Card(("♥","h"), 3)]
        self.assertEqual(self.ranker.rank(communityCards, hand), e.HANDRANK.FOUR_OF_A_KIND)

    def test_straight_flush(self):
        communityCards = [c.Card(("♠","s"), 2), c.Card(("♠","s"), 3), c.Card(("♠","s"), 6), c.Card(("♥","h"), 8) ]
        hand = [c.Card(("♠","s"), 4), c.Card(("♠","s"), 5)]
        self.assertEqual(self.ranker.rank(communityCards, hand), e.HANDRANK.STRAIGHT_FLUSH)

    def test_royal_flush(self):
        communityCards = [c.Card(("♣","c"), 1), c.Card(("♣","c"), 13), c.Card(("♠","s"), 6), c.Card(("♣","c"), 11) ]
        hand = [c.Card(("♣","c"), 10), c.Card(("♣","c"), 12)]
        self.assertEqual(self.ranker.rank(communityCards, hand), e.HANDRANK.ROYAL_FLUSH)

if __name__ == 'main':
    unittest.main()