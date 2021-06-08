space = ' '


class Token:
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos

    def __repr__(self):
        fmtstr = 'Token(word={},pos={})'
        result = fmtstr.format(repr(self.word), repr(self.pos))
        return result

    def __str__(self):
        result = '{}:{}'.format(self.pos, self.word)
        return result


def stringlist2tokenlist(list):
    result = []
    llist = len(list)
    for el in range(llist):
        thetoken = Token(list[el], el)
        result.append(thetoken)
    return result


def tokenlist2stringlist(tlist):
    result = [t.word for t in tlist]
    return result


def tokenlist2string(tlist):
    wordlist = [t.word for t in tlist]
    result = space.join(wordlist)
    return result


def show(tokenlist):
    resultlist = []
    for token in tokenlist:
        resultlist.append(str(token))
    result = ', '.join(resultlist)
    return result
