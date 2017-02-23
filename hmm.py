import numpy as np
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from hmmlearn import hmm

import utils

dictionary, X, lengths = utils.parseInput()

trainData = np.array([X]).reshape(-1, 1)
model = hmm.MultinomialHMM(n_components=10, n_iter=3, verbose=True)
model.fit(trainData, lengths=lengths)

def printSonnet(sonnet):
    for line in sonnet:
        words = [w for (w, _) in line]
        print ' '.join(words)
    print ' '

def generateNextWord((prevWord, prevState)):
    if not prevState:
        X, Z = model.sample(max(lengths))
        return (dictionary[X[0][0]], Z[0])
    else:
        transitions = model.transmat_[prevState]
        nextState = np.random.choice(len(transitions), p=transitions)
        nextWord = model._generate_sample_from_state(nextState)
        return (dictionary[nextWord[0]], nextState)

def checkLine(sonnet, currLine, line):
    if len(currLine) > 8:
        return "finished"
    else:
        return "valid"

def makeSonnet(model):
    sonnet = []
    currLine = []
    word = (None, None)
    line = 1
    while line <= 14:
        printSonnet(sonnet)
        nextWord = generateNextWord(word)
        currLine.append(nextWord)
        lineStatus = checkLine(sonnet, currLine, line)
        if lineStatus == "invalid":
            word = currLine.pop()
        elif lineStatus == "finished":
            sonnet.append(currLine)
            currLine = []
            line += 1
    printSonnet(sonnet)

makeSonnet(model)

sonnet = []
for _ in range(14):
    X, Z = model.sample(max(lengths))
    sonnet.append(' '.join([dictionary[i[0]] for i in X]))

for line in sonnet:
    print line
