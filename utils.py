def parseInput():
    dictionary = []
    dictMap = {}

    def dictionaryAdd(w):
        w = w.lower().strip(",.()':!?")
        if w not in dictMap:
            i = len(dictionary)
            dictMap[w] = i
            dictionary.append(w)
        return dictMap[w]

    X = []
    lengths = []

    def processSentence(sentence):
        words = sentence.split()
        for word in words:
            X.append(dictionaryAdd(word))
        lengths.append(len(words))

    sentence = [""]
    def processLine(line):
        if len(line) < 30:
            if len(sentence[0]) > 0:
                processSentence(sentence[0])
                sentence[0] = ""
        else:
            sentence[0] += " " + line.strip("\n")
            if line.strip("\n")[-1] in ".?!:":
                processSentence(sentence[0])
                sentence[0] = ""

    with open("shakespeare.txt", 'r') as f:
        for line in f:
            processLine(line)

    with open("spenser.txt", 'r') as f:
        for line in f:
            processLine(line)

    return dictionary, X, lengths
