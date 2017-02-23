def parseInput():
    dictionary = []
    dictMap = {}

    def dictionaryAdd(w):
        #w = w.lower().strip(",.()':")
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

    with open("shakespeare.txt", 'r') as f:
        for line in f:
            processLine(line)

    with open("spenser.txt", 'r') as f:
        for line in f:
            processLine(line)

    return dictionary, X, lengths
