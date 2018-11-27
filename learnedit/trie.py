class TrieNode:
  """Simple trie node.
  """
  def __init__(self):
    self.children = {}
    #does this terminate a dictionary entry?
    self.final = False
    #how many times was this prefix encountered while building the trie
    self.count = 1

class Trie:
  """Simple trie (prefix tree).
  """

  def __init__(self, epsilon=''):
    self.root = TrieNode()
    self.epsilon = epsilon

  def __iter__(self):
    stack = [(self.root, self.epsilon)]
    
    while stack:
      node, string = stack.pop()
      if node.final:
        yield string
      for char in node.children:
        stack.append((node.children[char], string + char))

  def _traverse(self, string, create_missing=False):
    node = self.root
    finals = set()
    traversed = self.epsilon
    if node.final:
      finals.add(traversed)

    for char in string:
      if char in node.children:
        child = node.children[char]
        if create_missing:
          child.count += 1
        node = child
      else:
        if create_missing:
          new_node = TrieNode()
          node.children[char] = new_node
          node = new_node
        else:
          break
      traversed += char
      if node.final:
        finals.add(traversed)

    return node, traversed, finals

  def add(self, string):
    """Add string to trie.
    """
    node, _, _ = self._traverse(string, True)
    node.final = True

  def prefixCount(self, string):
    """Count number of entries with this as a prefix.
    """
    node, traversed, _ = self._traverse(string, False)
    if traversed == string:
      return node.count
    else:
      return 0

  def prefixesOf(self, string):
    """Returns all entries that are prefixes of string.
    """
    node, traversed, finals = self._traverse(string, False)
    return finals

  def contains(self, string):
    """True if the string is contained as an entry.
    """

    node, traversed, _ = self._traverse(string, False)
    if traversed == string:
      return node.final
    else:
      return False

  def reversed(self):
    """Returns suffix trie (containing all entries, reversed).
    """
    ret = Trie(self.epsilon)
    for word in self:
      ret.add(word[::-1])
    return ret

