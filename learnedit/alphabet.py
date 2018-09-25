from . import trie
from gensim.models.phrases import Phrases, Phraser

class Alphabet:
  def __init__(self, arg1):
    if type(arg1) == trie.Trie:
      self.vocab = arg1
      self.vocab_reverse = arg1.reversed()
      self.epsilon = self.vocab.epsilon
    else:
      self._data_init(arg1)
  def _data_init(self, words):
    phrases = Phrases([list(w.replace('_','')) for w in words])
    normalized_phrases = {k.decode('utf-8').replace('_',''):v for k,v in phrases.vocab.items()}
    l1_phrases = [k for k in normalized_phrases if len(k) == 1]
    l2_phrase_scores = {k:v for k,v in normalized_phrases.items() if len(k) > 1}
    l2_phrases = sorted(l2_phrase_scores, key=lambda k:l2_phrase_scores[k], reverse=True)
    #TODO: determine best parameter for controlling bigram vocabulary
    #TODO: allow for n-grams?
    all_phrases = l1_phrases + l2_phrases[:len(l1_phrases)]
    self.vocab = trie.Trie()
    self.vocab_reverse = trie.Trie()
    for p in all_phrases:
      self.vocab.add(p)
      self.vocab_reverse.add(p[::-1])
  
  def __iter__(self):
    return iter(self.vocab)

  def forward(self):
    return self.vocab

  def reversed(self):
    return self.vocab_reverse



