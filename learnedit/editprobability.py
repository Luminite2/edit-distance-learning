import itertools
from collections import defaultdict
from . import trie

class EditProbability:
  def __init__(self, alph_x, alph_y):
    #two alphabets
    assert(type(alph_x) == trie.Trie)
    assert(type(alph_y) == trie.Trie)
    self.alph_x = alph_x
    self.alph_x_rev = alph_x.reverse()
    self.alph_y = alph_y
    self.alph_y_rev = alph_y.reverse()
    #probability storage
    self.probs = defaultdict(lambda:0.0)

  def _forward(self, x, y, a_x, a_y, probs):
    ret = defaultdict(lambda:0.0)
    ret[0,0] = 1.0
    for i in range(len(x)+1):
      for j in range(len(y)+1):
        for xi,yj in itertools.product(a_x.prefixesOf(x[i:]), a_y.prefixesOf(y[j:])):
          ret[i+len(xi),j+len(yj)] += probs[xi,yj]*ret[i,j]
    return ret

  def forward(self, x, y):
    return self._forward(x, y, self.alph_x, self.alph_y, self.probs)

  def backward(self, x, y):
    x_r = x[::-1]
    y_r = y[::-1]
    probs_r = {(a[::-1],b[::-1]):v for (a,b),v in self.probs.items()}
    probs_r = defaultdict(lambda:0.0,probs_r)
    ret_r = self._forward(x_r, y_r, self.alph_x_rev, self.alph_y_rev, probs_r)
    ret = type(ret_r)()
    for i,j in ret_r:
      ret[len(x)-i,len(y)-j] = ret_r[i,j]
    return ret

  def _eStep(self, x, y, accum):
    beta = self.backward(x, y)
    if beta[0,0] == 0.0:
      return accum
    alpha = self.forward(x, y)
    for i in range(len(x)+1):
      for j in range(len(y)+1):
        for xi,yj in itertools.product(self.alph_x.prefixesOf(x[i:]), self.alph_y.prefixesOf(y[j:])):
          accum[xi,yj] += self.probs[xi,yj] * alpha[i,j] * beta[i+len(xi),j+len(yj)] / beta[0,0]
    return accum


  def iterativeUpdate(self, data):
    #E-step
    gamma = defaultdict(lambda:0.0)
    for x,y in data:
      gamma = _eStep(x,y,gamma)
    #M-step
    N = 0.0
    for k in gamma:
      N += gamma[k]
    for k in gamma:
      gamma[k] /= N
    self.probs = gamma
    pass