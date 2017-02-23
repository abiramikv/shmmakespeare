import numpy as np
import warnings
from sklearn.externals import joblib

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from hmmlearn import hmm

import lang
import utils

dictionary, X, lengths = utils.parseInput()

trainData = np.array([X]).reshape(-1, 1)

try:
    model = joblib.load("model.pkl")
except:
    model = hmm.MultinomialHMM(n_components=10, n_iter=3, verbose=True)
    model.fit(trainData, lengths=lengths)

joblib.dump(model, "model.pkl")

def printSonnet(sonnet, currLine, nextWord):
    for line in sonnet:
        words = [w for (w, _) in line]
        print ' '.join(words)
    print ' '.join([w for (w, _) in currLine]), nextWord
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

def makeSonnet(model):
    sonnet = []
    currLine = []
    word = (None, None)
    line = 1
    while line <= 14:
        nextWord = generateNextWord(word)
        printSonnet(sonnet, currLine, nextWord)
        currLine.append(nextWord)
        lineStatus = lang.checkLine(sonnet, currLine, line)
        if lineStatus == "invalid":
            word = currLine.pop()
            word = currLine.pop()
            word = currLine.pop()
        elif lineStatus == "finished":
            sonnet.append(currLine)
            currLine = []
            line += 1
    printSonnet(sonnet)

makeSonnet(model)
