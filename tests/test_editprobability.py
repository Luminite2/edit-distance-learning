import unittest
from learnedit import EditProbability
from learnedit import Trie
from learnedit import Alphabet

class TestEditProbability(unittest.TestCase):

  def test_forward(self):
    tx = Trie()
    tx.add('')
    tx.add('a')
    ty = Trie()
    ty.add('b')
    ty.add('c')
    ty.add('bc')
    ty.add('')
    ep = EditProbability(Alphabet(tx),Alphabet(ty))
    ep.probs['a',''] = 0.5
    ep.probs['','b'] = 0.4
    ep.probs['','c'] = 0.3
    ep.probs['a','b'] = 0.2
    ep.probs['','bc'] = 0.1
    ep.probs['a', 'bc'] = 0.0
    ep.probs['a','c'] = 0.0
    r = ep.forward('a','bc')
    self.assertAlmostEqual(r[1,2],0.34)

  def test_backward(self):
    tx = Trie()
    tx.add('')
    tx.add('a')
    ty = Trie()
    ty.add('b')
    ty.add('c')
    ty.add('bc')
    ty.add('')
    ep = EditProbability(Alphabet(tx),Alphabet(ty))
    ep.probs['a',''] = 0.5
    ep.probs['','b'] = 0.4
    ep.probs['','c'] = 0.3
    ep.probs['a','b'] = 0.2
    ep.probs['','bc'] = 0.1
    ep.probs['a', 'bc'] = 0.0
    ep.probs['a','c'] = 0.0
    r = ep.backward('a','bc')
    self.assertAlmostEqual(r[0,0],0.34)

  def test_score(self):
    tx = Trie()
    tx.add('')
    tx.add('a')
    ty = Trie()
    ty.add('b')
    ty.add('c')
    ty.add('bc')
    ty.add('')
    ep = EditProbability(Alphabet(tx),Alphabet(ty))
    ep.probs['a',''] = 0.5
    ep.probs['','b'] = 0.4
    ep.probs['','c'] = 0.3
    ep.probs['a','b'] = 0.2
    ep.probs['','bc'] = 0.1
    ep.probs['a', 'bc'] = 0.0
    ep.probs['a','c'] = 0.0
    self.assertAlmostEqual(ep.score('a','bc'),0.34)

  def test_oov(self):
    tx = Trie()
    tx.add('')
    tx.add('a')
    ty = Trie()
    ty.add('b')
    ty.add('')
    ep = EditProbability(Alphabet(tx),Alphabet(ty))
    self.assertAlmostEqual(ep.score('a','bc'),0)

  def test_translit_xy(self):
    ep = EditProbability(Alphabet('','a','aa'),Alphabet('','b','c','bc'), lambda x,y: 0.0)
    ep.probs['a','b'] = 0.5
    ep.probs['aa','bc'] = 0.1
    x2y = ep.transliterator_x2y()
    self.assertEqual(x2y('aa'), 'bb')

  def test_translit_xy_missing(self):
    ep = EditProbability(Alphabet('','a','aa'),Alphabet('','b','c','bc'), lambda x,y: 0.0)
    ep.probs['a','b'] = 0.1
    ep.probs['aa','bc'] = 0.5
    x2y = ep.transliterator_x2y()
    self.assertEqual(x2y('a_a'), 'bb')

  def test_translit_yx(self):
    ep = EditProbability(Alphabet('','a','aa'),Alphabet('','b','c','bc'), lambda x,y: 0.0)
    ep.probs['a','c'] = 0.5
    ep.probs['a','b'] = 0.5
    ep.probs['','bc'] = 0.1
    y2x = ep.transliterator_y2x()
    self.assertEqual(y2x('bc'), 'aa')

  def test_translit_yx_missing(self):
    ep = EditProbability(Alphabet('','a','aa'),Alphabet('','b','c','bc'), lambda x,y: 0.0)
    ep.probs['a','c'] = 0.5
    ep.probs['a','b'] = 0.5
    ep.probs['','bc'] = 0.1
    y2x = ep.transliterator_y2x()
    self.assertEqual(y2x('b_c'), 'aa')

  def test_from_string(self):
    ep1 = EditProbability(Alphabet('','a'),Alphabet('','b'))
    ep1.probs['a',''] = 0.5
    ep2 = EditProbability.from_string(repr(ep1))
    self.assertCountEqual(ep1,ep2)
