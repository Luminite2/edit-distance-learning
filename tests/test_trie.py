import unittest
from learnedit import trie

class TestTrie(unittest.TestCase):
  def test_add_contains(self):
    t = trie.Trie()
    t.add('test')
    self.assertTrue(t.contains('test'))

  def test_add_contains_nested(self):
    t = trie.Trie()
    t.add('test')
    t.add('test2')
    self.assertTrue(t.contains('test'))
    self.assertTrue(t.contains('test2'))

  def test_add_contains_multiple(self):
    t = trie.Trie()
    t.add('one')
    t.add('two')
    self.assertTrue(t.contains('one'))
    self.assertTrue(t.contains('two'))

  def test_nocontain_prefixes(self):
    t = trie.Trie()
    t.add('one')
    self.assertFalse(t.contains('on'))

  def test_prefix_count(self):
    t = trie.Trie()
    t.add('test')
    t.add('test2')
    self.assertEqual(t.prefixCount('test'),2)

  def test_prefixes(self):
    t = trie.Trie()
    t.add('test')
    t.add('test2')
    t.add('test23')
    t.add('test4')
    self.assertCountEqual(t.prefixesOf('test23'),['test','test2','test23'])

  def test_add_contains_epsilon(self):
    t = trie.Trie()
    t.add('')
    self.assertTrue(t.contains(''))

  def test_prefixes_epsilon(self):
    t = trie.Trie()
    t.add('')
    self.assertCountEqual(t.prefixesOf(''),[''])

  def test_entries(self):
    t = trie.Trie()
    t.add('')
    t.add('test')
    t.add('test2')
    self.assertCountEqual(list(t),['','test','test2'])

  def test_reversed(self):
    t = trie.Trie()
    t.add('')
    t.add('abc')
    t.add('a')
    t.add('c')
    tr = t.reversed()
    self.assertCountEqual(list(tr),['','cba','a','c'])
