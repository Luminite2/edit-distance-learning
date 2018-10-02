import unittest
from learnedit import Alphabet
from learnedit import Trie

class TestAlphabet(unittest.TestCase):
  def test_init(self):
    a = Alphabet(['ab'])
    self.assertCountEqual(a,['','a','b','ab'])

  def test_init_reverse(self):
    a = Alphabet(['ab'])
    self.assertCountEqual(a.reversed(),['','a','b','ba'])

  def test_init_trie(self):
    t = Trie()
    t.add('ab')
    a = Alphabet(t)
    self.assertCountEqual(a,['ab'])
