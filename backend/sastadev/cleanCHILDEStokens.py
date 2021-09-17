import re
from copy import deepcopy

from sastadev import CHAT_Annotation, SDLOGGER, sastatok
from sastadev.metadata import Meta, bpl_none
from sastadev.sastatoken import show

hexformat = '\\u{0:04X}'


space = ' '

scope_open = '<'
scope_close = '>'

bstate, mstate, estate = 0, 1, 2

bstate, ostate, oostate, costate, ccstate = 0, 1, 2, 3, 4


def findscopeclose(tokens, offset=0):
    tokenctr = 0
    bracketcounter = -1
    begin = None
    end = None
    for token in tokens:
        if token.word == scope_open:
            if bracketcounter == -1:
                begin = tokenctr
            bracketcounter += 1
        elif token.word == scope_close:
            if bracketcounter == 0:
                end = tokenctr
                break
            else:
                bracketcounter -= 1
        else:
            pass
        tokenctr += 1
    result = (begin + offset, end + offset) if begin is not None and end is not None else None
    return result


def clearnesting(intokens, repkeep):
    tokens = deepcopy(intokens)
    bracketcounter = -1
    newtokens = []
    metadata = []
    bopenfound = False
    tokenctr = 0
    ltokens = len(tokens)
    while tokenctr < ltokens:
        token = tokens[tokenctr]
        if token.word == scope_open:
            begin = tokenctr
            span = findscopeclose(tokens[tokenctr:], offset=tokenctr)
            if span is None:
                SDLOGGER.error('Syntax error:Scope Open Symbol {} with position = {} ignored (no corresponding closing bracket) in:\n {}'.format(token.word, token.pos, show(tokens)))
            else:
                (begin, end) = span
                (midtokens, midmetadata) = cleantokens(tokens[begin + 1:end], repkeep)
                newtokens += [tokens[tokenctr]] + midtokens + [tokens[end]]
                metadata += midmetadata
                tokenctr = end
        elif token.word == scope_close:
            SDLOGGER.error('Syntax error: unexpected {} excountered with position {} in:\n {}'.format(token.word, token.pos, show(tokens)))
            newtokens.append(token)
        else:
            newtokens.append(token)
        tokenctr += 1
    return(newtokens, metadata)


def checkline(line, newline, outfilename, lineno, logfile):
    if checkpattern.search(newline) or pluspattern.search(newline):
        print(outfilename, lineno, 'suspect character', file=logfile)
        print('input=<{}>'.format(line[:-1]), file=logfile)
        print('output=<{}>'.format(newline), file=logfile)
        thecodes = str2codes(newline)
        print('charcodes=<{}>'.format(thecodes), file=logfile)


def cleantext(utt, repkeep):
    newutt = robustness(utt)
    tokens = sastatok.sasta_tokenize(newutt)
    inwordlist = [t.word for t in tokens]
    intokenstrings = [str(token) for token in tokens]
    # print(space.join(intokenstrings))
    (newtokens, metadata) = cleantokens(tokens, repkeep)
    resultwordlist = [t.word for t in newtokens]
    resultstring = smartjoin(resultwordlist)
    resultposlist = [t.pos for t in newtokens]
    newmeta1 = Meta('tokenisation', inwordlist, atype='list', source='CHAT/Tokenisation', backplacement=bpl_none)
    newmeta2 = Meta('cleanedtokenisation', resultwordlist, atype='list', source='CHAT/Tokenisation', backplacement=bpl_none)
    newmeta3 = Meta('cleanedtokenpositions', resultposlist, atype='list', source='CHAT/Tokenisation', backplacement=bpl_none)
    metadata += [newmeta1, newmeta2, newmeta3]
    resultmetadata = metadata
    return (resultstring, resultmetadata)


def cleantokens(tokens, repkeep):
    newtokens = deepcopy(tokens)
    metadata = []

    (newtokens, nestingmetadata) = clearnesting(newtokens, repkeep)
    metadata += nestingmetadata

    for annotation in CHAT_Annotation.annotations:
        (newtokens, annotationmetadata) = annotation.apply(newtokens, repkeep)
        metadata += annotationmetadata
        tokenstrings = [str(token) for token in newtokens]
        # print(space.join(tokenstrings))

    return (newtokens, metadata)


def str2codes(str):
    result = []
    for i in range(len(str)):
        curchar = str[i]
        curcode = hexformat.format(ord(str[i]))
        result.append((curchar, curcode))
    return(result)


def removesuspects(str):
    result1 = re.sub(checkpattern, space, str)
    result2 = re.sub(pluspattern1, r'\1', result1)
    result = re.sub(pluspattern2, r'\1', result2)
    return result


robustnessrules = [(re.compile(r'\[\+bch\]'), '[+bch]', '[+ bch]', 'Missing space'),
                   (re.compile(r'\[\+trn\]'), '[+trn]', '[+ trn]', 'Missing space'),
                   (re.compile(r'\[:(?![:\s])'), '[:', '[: ', 'Missing space'),
                   (re.compile(r'(?<=\w)\+\.\.\.'), '+...', ' +...', 'Missing space')
                   ]


def robustness(utt):
    newutt = utt
    for (regex, instr, outstr, msg) in robustnessrules:
        newnewutt = regex.sub(outstr, newutt)
        if newnewutt != newutt:
            SDLOGGER.warning('{}. Interpreted <{}> as <{}> in <{}>'.format(msg, instr, outstr, utt))
        newutt = newnewutt
    return newutt


# checkpattern = re.compile(r'[][\(\)&%@/=><_0^~↓↑↑↓⇗↗→↘⇘∞≈≋≡∙⌈⌉⌊⌋∆∇⁎⁇°◉▁▔☺∬Ϋ123456789·\u22A5\u00B7\u0001\u2260\u21AB]')
checkpattern = re.compile(r'[][\(\)&%@/=><_^~↓↑↑↓⇗↗→↘⇘∞≈≋≡∙⌈⌉⌊⌋∆∇⁎⁇°◉▁▔☺∬Ϋ·\u22A5\u00B7\u0001\u2260\u21AB\u2039\u203A]')
# + should not occur except as compound marker black+board
# next one split up in order to do substitutions
pluspattern = re.compile(r'(\W)\+|\+(\W)')
pluspattern1 = re.compile(r'(\W)\+')
pluspattern2 = re.compile(r'\+(\W)')


def test():
    repkeep = False
    teststr = {}
    testlist = [u'Dit een \u201Cquote en een \u2018inner quote\u2019 er ook nog bij\u201D ja en  los \u201D en \u2019 ja +..',
                r' hier is een (.) pauze, een langere (..), nog een langere (...) en een getimede (3.6) hier',
                r'dan nu wee [/?] weet ik [^c] dit is 0een ^nie nieuwe &*LAU:hmm clause',
                r' en [%xxx: wat is dat ] &eh www[>] maar mooi@a en [<] lelijk@x en myown@z:xxx en mooi [=? kooi] <heel iets> [?] anders',
                r'en < scope scopeend > [:: test] klaar',
                r'Das [: dat ] mooi@a een [/] een en < scope scopeend > [:: test] en [=? x] wat [?] helemaal opnieuw [///] drie [x 3 ] mooi [= beautiful] en dan [% commentaar ]'
                r'Das [: dat is ] is  @ab xxx en <Pikkie Paus> [: Mickey Mouse] en  &+uh en  (ge)kocht  klaar ',
                r'Das [: dat is ] is een [/] een <ja een> [/] ja een @ab xxx en <Pikkie Paus> [: Mickey Mouse] en yyy en www  maar &+uh en [/] (ge)kocht boeke(n) ei(gen)lijk klaar ',
                r'Dat [:: dit] (i)s 0toch &he niet [x 3] zo efoudig [: eenvoudig], hoor!',
                r'Dat (i)s 0toch &he niet [x 3] zo efoudig [: heel eenvoudig], hoor!',
                r'Nu <een of twee> [=? een twee] of toch [?] <heel iets> [?] anders',
                r'ja <ik wil> [/] ik wil graag doch [//] toch iest [: iets] anders [% commentaar] doen',
                r'dat < kan &he iets >[/] en < ja <nog me> [//] nog meer > te doen> hoor!']
    i = 0
    for el in testlist:
        teststr[i] = el
        i += 1

    for i in teststr:
        print(teststr[i])
        intokens = sastatok.sasta_tokenize(teststr[i])
        intokenstrings = [str(token) for token in intokens]
        print(space.join(intokenstrings))
        (newtokens, metadata) = cleantext(teststr[i], repkeep)
        tokenstrings = [str(token) for token in newtokens]
        print(space.join(tokenstrings))
        # mdstrs = [str(m) for m in metadata]
        # print(space.join(mdstrs))
        for m in metadata:
            print(str(m))
        print('')


def ispunctuation(wrd):
    result = wrd in '.?!;,!<>'
    return result


def smartjoin(strings):
    result = ''
    lstrings = len(strings)
    if lstrings > 0:
        for i in range(lstrings - 1):
            if ispunctuation(strings[i + 1]):
                result += strings[i]
            else:
                result += strings[i] + space
        result += strings[lstrings - 1]
    return result
