import numpy as np
from hmmlearn import hmm

dictionary = []
dictMap = {}
i = 0

def dictionaryAdd(w):
    global i
    if w not in dictMap:
        dictMap[w] = i
        dictionary.append(w)
        i += 1
    return dictMap[w]

X = []
maxLength = 0

def processLine(line):
    global maxLength
    if len(line) < 30:
        return
    tokens = [dictionaryAdd(w) for w in line.split()]
    maxLength = max(maxLength, len(tokens))
    X.append(tokens)

with open("shakespeare.txt", 'r') as f:
    for line in f:
        processLine(line)

with open("spenser.txt", 'r') as f:
    for line in f:
        processLine(line)

for i in range(len(X)):
    X[i] = X[i] + [-1] * (maxLength - len(X[i]))

model = hmm.GaussianHMM(n_components=30, n_iter=20)
model.fit(X)
# >>> model.means_ = np.array([[0.0, 0.0], [3.0, -3.0], [5.0, 10.0]])
# >>> model.covars_ = np.tile(np.identity(2), (3, 1, 1))
X, Z = model.sample(100)
print ' '.join([dictionary[i] for i in Z])
