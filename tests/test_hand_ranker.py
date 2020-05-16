import unittest
import context

from core import handRanker
from core import core as c
from core import enums as e

class TestCore(unittest.TestCase):
    def setUp(self):
        self.ranker = handRanker.HandRanker()

    def test_high_card(self):
        hand = [c.Card(("♣","c"), "K"), c.Card(("♣","c"), "2") ]
        self.assertEqual( self.ranker.rank(None, hand), e.HANDRANK.HIGH_CARD)

    def test_pair(self):
        hand = [c.Card(("♣","c"), "K"), c.Card(("♠","s"), "K") ]
        self.assertEqual( self.ranker.rank(None, hand), e.HANDRANK.PAIR)

if __name__ == 'main':
    unittest.main()