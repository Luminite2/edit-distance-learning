#from . import trie
from . import Trie
#import trie
from gensim.models.phrases import Phrases

class Alphabet:
  def __init__(self, *args, **kwargs):
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
      self._data_init(args[0], **kwargs)
    self.epsilon = self.vocab.epsilon


  def __repr__(self):
    return 'Alphabet({})'.format(','.join([repr(a) for a in sorted(self)]))

  def __len__(self):
    return len(self.vocab)

  @staticmethod
  def from_string(s):
    return eval(s)

  def _data_init(self, words, **kwargs):
    #phrases = Phrases([list(w) for w in words])
    #normalized_phrases = {k.decode('utf-8'):v for k,v in phrases.vocab.items()}
    _,vocab_counts,_ = Phrases.learn_vocab(words,2000,delimiter=b'')
    unigram_scores = {k.decode('utf-8'):v for k,v in vocab_counts.items() if len(k) == 1}
    ngram_scores = {k.decode('utf-8'):v for k,v in vocab_counts.items() if len(k) > 1}
    unigrams = sorted(unigram_scores, key=lambda k:unigram_scores[k], reverse=True)
    ngrams = sorted(ngram_scores, key=lambda k:ngram_scores[k], reverse=True)
    unigram_limit = len(unigrams)
    if 'unigram_limit' in kwargs:
      unigram_limit = kwargs['unigram_limit']
    #TODO: determine best parameter for controlling bigram vocabulary
    #TODO: allow for n-grams?
    #all_phrases = l1_phrases + l2_phrases[:len(l1_phrases)]
    all_phrases = unigrams[:unigram_limit] + ngrams[:unigram_limit] #TODO: determine bigram number some other way?
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



