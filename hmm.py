import numpy as np

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from hmmlearn import hmm

dictionary = []
dictMap = {}
i = 0

def dictionaryAdd(w):
    global i
    w = w.lower().strip(",.")
    if w not in dictMap:
        dictMap[w] = i
        dictionary.append(w)
        i += 1
    return dictMap[w]

X = []
lengths = []

def processLine(line):
    global X, maxLength
    if len(line) < 30:
        return
    tokens = [dictionaryAdd(w) for w in line.split()]
    X += tokens
    lengths.append(len(tokens))

with open("shakespeare.txt", 'r') as f:
    for line in f:
        processLine(line)

with open("spenser.txt", 'r') as f:
    for line in f:
        processLine(line)

trainData = np.array([X]).reshape(-1, 1)
model = hmm.GaussianHMM(n_components=10, n_iter=20, verbose=True)
model.fit(trainData, lengths=lengths)

sonnet = []
for _ in range(14):
    X, Z = model.sample(max(lengths))
    sonnet.append(' '.join([dictionary[i] for i in Z]))

for line in sonnet:
    print line
