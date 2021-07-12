import re

from sastadev.sastatok import fullre, fullsastare, myrepetition, sasta_tokenize

teststr = {}
teststr[1] = r'Dat [:: dit] (i)s 0toch &he niet [x 3] zo efoudig [: eenvoudig], hoor!'
teststr[2] = r'Dat (i)s 0toch &he niet [x 3] zo efoudig [: heel eenvoudig], hoor!'
teststr[3] = r'Nu <een of twee> [=? een twee] of toch [?] <heel iets> [?] anders'
teststr[4] = r'ja <ik wil> [/] ik wil graag doch [//] toch iest [: iets] anders [% commentaar] doen'


def test_sastatok():
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
