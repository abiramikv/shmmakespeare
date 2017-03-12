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

def printSonnet(sonnet):
    for i, line in enumerate(sonnet):
        padding = ''
        if i > 11:
            padding = '  '
        words = ["\\textcolor{" + str(s) + "}{" + w + "}" for w, s in line]
        # words = [w for (w, _) in line]
        # words[0] = words[0].capitalize()
        print(padding + ' '.join(words))
    # print ' '.join([w for (w, _) in currLine]), nextWord
    print ' '

def generateNextWord((prevWord, prevState)):
    nextState = None
    nextWord = None
    while nextWord == None or dictionary[nextWord] == prevWord:
        if not prevState:
            X, Z = model.sample(max(lengths))
            nextState = Z[0]
            nextWord = X[0][0]
        else:
            transitions = model.transmat_[prevState]
            nextState = np.random.choice(len(transitions), p=transitions)
            nextWord = model._generate_sample_from_state(nextState)[0]
    return (dictionary[nextWord], nextState)

def makeSonnet(model):
    sonnet = []
    currLine = []
    word = (None, None)
    line = 1
    while line <= 14:
        nextWord = generateNextWord(word)
        printSonnet(sonnet)
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

def visualizeStates(states):
    for state in states:
        x = sorted(enumerate(model.emissionprob_[state]), key = lambda x: x[1])[-10:]
        print " ".join(map(lambda y: dictionary[y[0]], reversed(x)))

        print ''

def visualizeWords(words):
    partitions = [[] for _ in range(10)]
    for i, x in enumerate(dictionary):
        probs = map(lambda state: model.emissionprob_[state][i], range(10))
        j = np.argmax(probs)
        partitions[j].append((probs[j], x))
    for partition in partitions:
        partition.sort(reverse=True)
        print ' '.join(map(lambda t: t[1], partition[:10]))

makeSonnet(model)
#visualizeStates(range(10))
#visualizeWords(set(["desolate", "love", "heart", "learn", "run", "beauty", "rosy", "confused", "labour", "cup", "time", "rise", "sea"]))
