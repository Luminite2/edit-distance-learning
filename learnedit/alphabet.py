#from . import trie
from . import Trie
#import trie
from gensim.models.phrases import Phrases, Phraser

class Alphabet:
  def __init__(self, *args):
    self.vocab = Trie()
    self.vocab_reverse = Trie()
    if len(args) == 0:
      self.vocab.add('')
      self.vocab_reverse.add('')
    elif type(args[0]) == Trie:
      self.vocab = args[0]
      self.vocab_reverse = args[0].reversed()
    elif type(args[0]) == str:
      for char in args:
        self.vocab.add(char)
        self.vocab_reverse.add(char[::-1])
    else:
      self._data_init(args[0])
    self.epsilon = self.vocab.epsilon


  def __repr__(self):
    return 'Alphabet({})'.format(','.join([repr(a) for a in sorted(self)]))

  @staticmethod
  def from_string(s):
    return eval(s)

  def _data_init(self, words):
    phrases = Phrases([list(w.replace('_','')) for w in words])
    normalized_phrases = {k.decode('utf-8').replace('_',''):v for k,v in phrases.vocab.items()}
    l1_phrases = [k for k in normalized_phrases if len(k) == 1]
    l2_phrase_scores = {k:v for k,v in normalized_phrases.items() if len(k) > 1}
    l2_phrases = sorted(l2_phrase_scores, key=lambda k:l2_phrase_scores[k], reverse=True)
    #TODO: determine best parameter for controlling bigram vocabulary
    #TODO: allow for n-grams?
    all_phrases = l1_phrases + l2_phrases[:len(l1_phrases)]
    #self.vocab = trie.Trie()
    #self.vocab_reverse = trie.Trie()
    self.vocab.add('') #optional?
    self.vocab_reverse.add('')
    for p in all_phrases:
      self.vocab.add(p)
      self.vocab_reverse.add(p[::-1])
  
  def __iter__(self):
    return iter(self.vocab)

  def forward(self):
    return self.vocab

  def reversed(self):
    return self.vocab_reverse



