import numpy as np
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from hmmlearn import hmm

dictionary = []
dictMap = {}

def dictionaryAdd(w):
    w = w.lower().strip(",.()':!?;")
    if w not in dictMap:
        i = len(dictionary)
        dictMap[w] = i
        dictionary.append(w)
    return dictMap[w]

X = []
lengths = []

def processLine(line):
    if len(line) < 30:
        return
    words = line.split()
    for word in words:
        X.append(dictionaryAdd(word))
    lengths.append(len(words))

with open("test.txt", 'r') as f:
    for line in f:
        processLine(line)

trainData = np.array([X]).reshape(-1, 1)

model = hmm.MultinomialHMM(n_components=10, n_iter=2, verbose=True)
model.fit(trainData, lengths=lengths)

def visualizeStates(states):
    for state in states:
        x = sorted(enumerate(model.emissionprob_[state]), key = lambda x: x[1])[-10:]
        print " ".join(map(lambda y: dictionary[y[0]], reversed(x)))

        print ''

visualizeStates(range(10))
X, Z = model.sample(20)
print " ".join(map(lambda x: dictionary[x[0]], X))
print(Z)
