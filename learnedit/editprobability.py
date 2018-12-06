import itertools
from collections import defaultdict
#from . import trie
#from . import alphabet
#import alphabet
from . import Alphabet

class EditProbability:
  #TODO: allow init from data directly
  def __init__(self, alph_x, alph_y, initf=lambda x,y: 0.5):
    import types
    #two alphabets
    assert(type(alph_x) == Alphabet)
    assert(type(alph_y) == Alphabet)
    self.alph_x = alph_x
    self.alph_x_rev = alph_x.reversed()
    self.alph_y = alph_y
    self.alph_y_rev = alph_y.reversed()
    #probability storage
    self.probs = defaultdict(lambda:0.0)
    for x,y in self._product(alph_x,alph_y):
      if type(initf) == types.FunctionType:
        self.probs[x,y] = initf(x,y)
      elif (x,y) in initf:
        self.probs[x,y] = initf[x,y]

  def __str__(self):
    ret = '{\n'
    for a,b in sorted(self.probs,key=lambda k: self.probs[k], reverse=True):
      ret += '\t({},{}): {}\n'.format(a,b,self.probs[a,b])
    ret += '}\n'
    return ret

  def __repr__(self):
    args = ''
    ax = repr(self.alph_x)
    ay = repr(self.alph_y)
    init_dict = {}
    for a,b in sorted(self.probs,key=lambda k: self.probs[k], reverse=True):
      init_dict[a,b] = self.probs[a,b]
    return 'EditProbability({},{},{})'.format(ax,ay,init_dict)

  @staticmethod
  def from_string(s):
    return eval(s)

  @staticmethod
  def from_file(fname):
    with open(fname, 'r', encoding='utf-8', errors='surrogateescape') as f:
      return EditProbability.from_string(f.read())

  def _product(self,xs,ys):
    for x,y in itertools.product(xs,ys):
      if x == self.alph_x.epsilon and y == self.alph_y.epsilon:
        continue
      yield x,y

  def _forward(self, x, y, a_x, a_y, probs):
    ret = defaultdict(lambda:0.0)
    ret[0,0] = 1.0
    for i in range(len(x)+1):
      for j in range(len(y)+1):
        for xi,yj in self._product(a_x.prefixesOf(x[i:]), a_y.prefixesOf(y[j:])):
          ret[i+len(xi),j+len(yj)] += probs[xi,yj]*ret[i,j]
    return ret

  def forward(self, x, y):
    return self._forward(x, y, self.alph_x.forward(), self.alph_y.forward(), self.probs)

  def backward(self, x, y):
    x_r = x[::-1]
    y_r = y[::-1]
    probs_r = {(a[::-1],b[::-1]):v for (a,b),v in self.probs.items()}
    probs_r = defaultdict(lambda:0.0,probs_r)
    ret_r = self._forward(x_r, y_r, self.alph_x.reversed(), self.alph_y.reversed(), probs_r)
    #ret = type(ret_r)()
    ret = defaultdict(lambda:0.0)
    for i,j in ret_r:
      ret[len(x)-i,len(y)-j] = ret_r[i,j]
    return ret

  def _eStep(self, x, y, accum):
    beta = self.backward(x, y)
    if beta[0,0] == 0.0: return accum
    alpha = self.forward(x, y)
    for i in range(len(x)+1):
      for j in range(len(y)+1):
        for xi,yj in itertools.product(self.alph_x.forward().prefixesOf(x[i:]), self.alph_y.forward().prefixesOf(y[j:])):
          accum[xi,yj] += self.probs[xi,yj] * alpha[i,j] * beta[i+len(xi),j+len(yj)] / beta[0,0]
    return accum

  def iterativeUpdate(self, data):
    #E-step
    gamma = defaultdict(lambda:0.0)
    for x,y in data:
      gamma = self._eStep(x,y,gamma)
    #M-step
    N = 0.0
    for k in gamma:
      N += gamma[k]
    for k in gamma:
      gamma[k] /= N
    self.probs = gamma

  def score(self, x, y):
    return self.forward(x,y)[len(x),len(y)]
  
  def save(self, fname):
    with open(fname,'w',encoding='utf-8',errors='surrogateescape') as f:
      f.write(repr(self))

  def __iter__(self):
    for a,b in self.probs:
      yield ((a,b),self.probs[a,b])

  def _transliterator(self, alph, x2y, probs):
    import math
    def transliterate(word):
      N = len(word)
      dp_table = [-float('inf') for _ in range(N+1)]
      dp_table[0] = 0.0
      #bp_table = ['' for _ in range(N+1)]
      bp_table = ['']
      bp_table.extend(list(word))
      for i in range(1,N+1):
        candidate_xs = [rev_ngram[::-1] for rev_ngram in alph.reversed().prefixesOf(word[:i][::-1])]
        for cx in candidate_xs:
          if len(cx) == 0:
            continue
          cy = x2y[cx]
          if probs(cx,cy) > 0.0:
            log_prob = math.log(probs(cx,cy)) + dp_table[i-len(cx)]
            if log_prob >= dp_table[i]:
              dp_table[i] = log_prob
              bp_table[i] = cx
      result = ''
      i = N
      while i > 0:
        result = x2y[bp_table[i]] + result
        i -= max(1,len(bp_table[i]))
      return result

    return transliterate


  def transliterator_x2y(self):
    #version 1: greedily find bigrams

    x2y = defaultdict(lambda: self.alph_y.epsilon)
    for x in self.alph_x.forward():
      p_max = 0.0
      y_max = x
      for y in self.alph_y.forward():
        if self.probs[x,y] >= p_max:
          p_max = self.probs[x,y]
          y_max = y
      x2y[x] = y_max

    return self._transliterator(self.alph_x, x2y, lambda x,y: self.probs[x,y])

  def transliterator_y2x(self):

    y2x = defaultdict(lambda: self.alph_x.epsilon)
    for y in self.alph_y.forward():
      p_max = 0.0
      x_max = y
      for x in self.alph_x.forward():
        if self.probs[x,y] >= p_max:
          p_max = self.probs[x,y]
          x_max = x
      y2x[y] = x_max

    return self._transliterator(self.alph_y, y2x, lambda y,x: self.probs[x,y])
