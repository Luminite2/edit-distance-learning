import unittest
from learnedit import alphabet

class TestAlphabet(unittest.TestCase):
  def test_init(self):
    a = alphabet.Alphabet(['ab'])
    self.assertCountEqual(a,['a','b','ab'])

  def test_init_reverse(self):
    a = alphabet.Alphabet(['ab'])
    self.assertCountEqual(a.reversed(),['a','b','ba'])
