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

  def test_init_alph(self):
    a = Alphabet('a','')
    self.assertCountEqual(a,['','a'])

  def test_repr(self):
    a = Alphabet('a','b','\'',',','')
    self.assertEqual(repr(a),'Alphabet(\'\',\"\'\",\',\',\'a\',\'b\')')

  def test_from_string(self):
    a = Alphabet('a','b','\'',',','')
    b = Alphabet.from_string(repr(a))
    self.assertCountEqual(a,b)

  def test_iter(self):
    a = Alphabet('a','b')
    self.assertCountEqual(a,['a','b'])
