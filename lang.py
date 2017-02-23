from nltk.corpus import cmudict

words = cmudict.dict()

def numSyllables(word):
    count = 0
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']

    # first attempt to use NLTK database
    if word in words:

        count = len(list(phoneme for phoneme in words[word][0] if phoneme[-1].isdigit()))

    # otherwise use own algorithm if word not found in cmudict
    else:
        if word[0] in vowels:
            count += 1
        for i in range(len(word) - 1):
            if word[i] not in vowels and word[i+1] in vowels:
                count += 1
        if word[-1] == 'e':
            count -= 1
        if count == 0:
            count += 1

    return count

# returns true if words rhyme, false if they do not or they are not found in dictionary
def checkRhyme(word1, word2, level):
    if word1 in words and word2 in words:
        phon1 = words[word1]
        phon2 = words[word2]

        if min(len(phon1[0]), len(phon2)) < level:
            level = min(len(phon1[0]), len(phon2))

        for version1 in phon1:
            for version2 in phon2:
                if version1[-level:] == version2[-level:]:
                    print(version1[-level:], version2[-level:])
                    return True
    return False

def checkLine(sonnet, currLine, line):
    sylCount = 0
    for word, _ in currLine:
        sylCount += numSyllables(word)


    if sylCount == 10:
        if line > 12:
            if line == 13:
                rhymes = True
            else:
                rhymes = checkRhyme(currLine[-1], sonnet[line-1][-1], 2)
        else:
            if line in [1, 2, 5, 6, 9, 10]:
                rhymes = True
            else:
                rhymes = checkRhyme(currLine[-1], sonnet[line-2][-1], 2)
        if rhymes:
            return "finished"
        else:
            return "invalid"
    if sylCount > 10:
        return "invalid"
    else:
        return "valid"
