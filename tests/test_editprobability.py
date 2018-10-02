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
