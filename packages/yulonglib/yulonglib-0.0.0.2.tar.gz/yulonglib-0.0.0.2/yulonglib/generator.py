import collections
class Generator(object):
    def __init__(self,seq=[]):
        self.seqs=collections.deque()
        self.seqs.append(seq)
    def __iter__(self):
        while self.seqs:
            seq = self.seqs.popleft()
            for i in seq:
                yield i
    def update(self,seq2):
        self.seqs.append(seq2)
    def append(self,seq2):
        self.seqs.append((seq2,))
