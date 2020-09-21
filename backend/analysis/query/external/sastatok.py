from .sastatoken import stringlist2tokenlist
from .CHAT_Annotation import CHAT_patterns, wordpat, interpunction
import re


def alts(pats, grouping=False):
    result = r''
    for pat in pats:
        if result == r'':
            result = pat
        else:
            result += '|' + pat
    if grouping:
        result = '(' + result + ')'
    else:
        result = '(?:' + result + ')'
    return result


# interpunction = r'[!\?\.,;]'  # add colon separated by spaces
# word = r'[^!\?;\.\[\]<>\s]+'
word = wordpat
scope = r'<.+?>'
scopeorword = alts([scope, word])
myrepetition = r'\[x\s*[0-9]+\s*\]'
replacement = scopeorword + r'\s*\[:.+?\]'
realwordreplacement = scopeorword + r'\s*\[::.+?\]'
alternativetranscription = r'\[=\?.+?\]'
# dependenttier # p. 71
commentonmainline = r'\[%.+?\]'  # p. 71
# bestguess = scopeorword+r'\s*\[\?\]' #p. 70-71
bestguess = r'\[\?\]'
# overlap follows p. 71
# overlap precedes p. 71
repetition = scopeorword + r'\s*\[/\]\s*' + word  # p73 should actually cover the number of words inside the scope
retracing = scopeorword + r'\s*\[//\]\s*' + word  # p73
whitespace = r'\s+'


# sastaspecials = [r'\[::', r'\[=', r'\[:', r'\[=\?', r'\[x', r'\<', r'\>', r'\[\?\]', r'\[/\]', r'\[//\]', r'\[///\]', r'\[%', r'\]']
sastaspecials = list(CHAT_patterns)
sastapatterns = sorted(sastaspecials, key=lambda x: len(x), reverse=True) + [word, interpunction]
fullsastapatterns = alts(sastapatterns)
fullsastare = re.compile(fullsastapatterns)

allpatterns = [realwordreplacement, replacement, myrepetition, alternativetranscription, commentonmainline, bestguess, retracing]
sortedallpatterns = sorted(allpatterns, key=lambda x: len(x), reverse=True) + [word, interpunction]
fullpattern = alts(sortedallpatterns)
# print(fullpattern)
fullre = re.compile(fullpattern)


def tokenize(instring):
    tokenstring = fullre.findall(instring)
    result = stringlist2tokenlist(tokenstring)
    return result


def sasta_tokenize(instring):
    tokenstring = fullsastare.findall(instring)
    result = stringlist2tokenlist(tokenstring)
    return result


teststr = {}
teststr[1] = r'Dat [:: dit] (i)s 0toch &he niet [x 3] zo efoudig [: eenvoudig], hoor!'
teststr[2] = r'Dat (i)s 0toch &he niet [x 3] zo efoudig [: heel eenvoudig], hoor!'
teststr[3] = r'Nu <een of twee> [=? een twee] of toch [?] <heel iets> [?] anders'
teststr[4] = r'ja <ik wil> [/] ik wil graag doch [//] toch iest [: iets] anders [% commentaar] doen'

if __name__ == '__main__':
    tokens = re.findall(myrepetition, 'aap [x 3] noot')
    print('reptest', tokens)
    for i in teststr:
        tokens = fullre.findall(teststr[i])
        print(tokens)

    print('Sasta:')

    for i in teststr:
        tokens = fullsastare.findall(teststr[i])
        print(tokens)

    for i in teststr:
        tokens = sasta_tokenize(teststr[i])
        for token in tokens:
            print('{}:{}'.format(token.pos, token.word), end=' ')
        print('')
