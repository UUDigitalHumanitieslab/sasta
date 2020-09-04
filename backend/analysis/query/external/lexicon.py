from . import celexlexicon

space = ' '
celex = 'celex'
alpino = 'alpino'

lexicon = celex


def getwordinfo(word):
    results = []
    if lexicon == celex:
        results = celexlexicon.getwordinfo(word)
    return results


def informlexicon(word):
    allwords = word.split(space)
    result = True
    for aword in allwords:
        if lexicon == 'celex':
            result = result and celexlexicon.incelexdmw(aword)
        elif lexicon == 'alpino':
            result = False
        else:
            result = False
    return result


def test():
    testwords = ['stukkies', 'jochie', 'gevalt', 'stukjes',
                 'gevallen', 'mouwe', 'mouwen', 'gaatie', 'gaat', 'ie']
    for w in testwords:
        print(w, informlexicon(w))


if __name__ == '__main__':
    test()
