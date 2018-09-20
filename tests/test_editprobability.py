import unittest
from learnedit import editprobability
from learnedit import trie

class TestEditProbability(unittest.TestCase):

  def test_forward(self):
    ax = trie.Trie()
    ax.add('')
    ax.add('a')
    ay = trie.Trie()
    ay.add('b')
    ay.add('c')
    ay.add('bc')
    ay.add('')
    ep = editprobability.EditProbability(ax,ay)
    ep.probs['a',''] = 0.5
    ep.probs['','b'] = 0.4
    ep.probs['','c'] = 0.3
    ep.probs['a','b'] = 0.2
    ep.probs['','bc'] = 0.1
    r = ep.forward('a','bc')
    self.assertAlmostEqual(r[1,2],0.34)

  def test_backward(self):
    ax = trie.Trie()
    ax.add('')
    ax.add('a')
    ay = trie.Trie()
    ay.add('b')
    ay.add('c')
    ay.add('bc')
    ay.add('')
    ep = editprobability.EditProbability(ax,ay)
    ep.probs['a',''] = 0.5
    ep.probs['','b'] = 0.4
    ep.probs['','c'] = 0.3
    ep.probs['a','b'] = 0.2
    ep.probs['','bc'] = 0.1
    r = ep.backward('a','bc')
    self.assertAlmostEqual(r[0,0],0.34)
