from sastadev.sastatoken import Token, show
from sastadev.metadata import Meta
from sastadev import cleanCHILDEStokens
import re

from sastadev import SDLOGGER

CHAT = 'CHAT'

monadic = 1
dyadic = 2

emptyregex = r''
eps = ''
space = ' '
keep = r'\0'
restart = 'restart'
scope_open = '<'
scope_close = '>'
emptyreplacement = eps
anybutrb = r'[^\]]*'


def fullre(pat):
    result = r'^' + pat + r'$'
    return result


def identity(x):
    return x


def refunction(x):
    '''
    The input regular expression is adapted to the requirements, surrounded by ^ and $ (see refunction)
    :param x: a regular expression
    :return: a modified regular expression
    '''
    result = fullre(x)
    return result


# states
bstate, mstate, estate = 0, 1, 2
scopestate, scopefoundstate, wstate, rfoundstate = 11, 12, 13, 14
wordinitial = r'[\w\'\(\)' + u'\u2019\u02C8\u02CC\u02de\u21AB\u2260' + r']'
wordpat = wordinitial + r'[\w:\^\+_~\'\-\(\)' + u'\u2019\u02C8\u02CC\u0329\u02de\u21AB\u2260' + r']*'  # removed \. here in the second part maybe needed for (.)?
simplewordpat = r'\w+'
fullwordpat = fullre(wordpat)
wordre = re.compile(fullwordpat)
# interpunction = r'(:?' + r'[!\?\.,;]' + '|' + u'[\u201C\u201D\u2039\u203A]' + r'|' + r'(?<=\s):' + r')'
interpunction = r'\-\-\-|\-\-|\-|\-' + r'|' + r'[!\?\.,;]' + '|' + u'[\u201C\u201D\u2039\u203A]' + r'|' + r'(?<=\s):'
filenamepat = r'[\w\.]+'
fullfilenamepat = fullre(filenamepat)
fullfilenamere = re.compile(fullfilenamepat)

wordorpuncpat = r'(:?' + wordpat + '|' + interpunction + ')'

specialformpat = wordpat + r'(?:@z:\w\w\w|@\w\w?\w?)'
fullspecialformpat = fullre(specialformpat)
specialformre = re.compile(fullspecialformpat)
repkeepannotations = ['Repetition', 'Retracing', 'Reformulation']


def getreplacement(repkeep, annotation):
    if annotation.name in repkeepannotations:
        if repkeep:
            replacement = keep
        else:
            replacement = eps
    else:
        replacement = annotation.regex.replacement
    return replacement


def doreplacement(repltokens, replacement, tokens):
    newtokens = tokens
    if replacement == keep:
        newtokens += repltokens
    elif replacement == eps:
        pass
    else:
        SDLOGGER.error('Unknown replacement: {}'.format(replacement))
    return newtokens


class CHAT_Annotation:
    def __init__(self, name, v2015, v2020, regex, metadatafunction, message=None):
        self.name = name
        self.v2015 = v2015
        self.v2020 = v2020
        self.regex = regex
        self.metadatafunction = metadatafunction
        self.message = message

    def apply(self, tokens, repkeep=False):
        (newtokens, metadata) = self.regex.apply(tokens, self, repkeep)
        if self.message is not None:
            self.message(self.name, show(tokens))
        return (newtokens, metadata)


def isaword(wrd):
    match = wordre.search(wrd)
    result = match is not None
    return result


class CHAT_Regex:
    def __init__(self):
        pass


class CHAT_InWordRegex(CHAT_Regex):
    def __init__(self, regex, replacement):
        self.regex = regex
        self.replacement = replacement
        self.compiledre = re.compile(identity(self.regex))

    def apply(self, tokens, annotation, repkeep):
        newtokens = []
        metadata = []
        insidebrackets, outsidebrackets = 0, 1
        state = outsidebrackets
        for token in tokens:
            if isaword(token.word):
                if state == outsidebrackets:
                    matches = self.compiledre.finditer(token.word)
                    for m in matches:
                        annotationwordlist = [m.group()]
                        annotatedposlist = [token.pos]
                        annotatedwordlist = [token.word]
                        annotationposlist = [p for p in range(m.start(), m.end())]
                        newmeta = annotation.metadatafunction(annotation, annotationwordlist, annotatedposlist, annotatedwordlist, annotationposlist)
                        metadata.append(newmeta)
                    newword = self.compiledre.sub(self.replacement, token.word)
                    newtoken = Token(newword, token.pos)
                else:
                    newtoken = token
            elif isopenbracket(token.word):
                state = insidebrackets
                newtoken = token
            elif isclosebracket(token.word):
                state = outsidebrackets
                newtoken = token
            else:
                newtoken = token
            if newtoken.word != "":
                newtokens.append(newtoken)
        return (newtokens, metadata)


class CHAT_SimpleRegex(CHAT_Regex):
    def __init__(self, regex, replacement, scoped):
        self.regex = regex
        self.replacement = replacement
        self.scoped = scoped
        self.compiledre = re.compile(refunction(self.regex))

    def apply(self, tokens, annotation, repkeep):
        newtokens = []
        metadata = []
        insidebrackets, outsidebrackets = 0, 1
        state = outsidebrackets
        for token in tokens:
            if self.compiledre.search(token.word):
                if state == outsidebrackets:
                    if self.replacement == keep:
                        newtoken = token
                        newtokens.append(newtoken)
                    elif callable(self.replacement):
                        newtokenword = self.replacement(token.word)
                        newtoken = Token(newtokenword, token.pos)
                        newtokens.append(newtoken)
                    elif isinstance(self.replacement, str):
                        newtokenword = self.compiledre.sub(self.replacement, token.word)
                        if newtokenword != '':
                            newtoken = Token(newtokenword, token.pos)
                            newtokens.append(newtoken)
                        else:
                            pass  # token is removed
                    else:
                        pass  # token is removed
                    metadata.append(annotation.metadatafunction(annotation, token.pos, token.word))
                else:
                    newtokens.append(token)
            elif isopenbracket(token.word):
                state = insidebrackets
                newtokens.append(token)
            elif isclosebracket(token.word):
                state = outsidebrackets
                newtokens.append(token)
            else:
                newtokens.append(token)

        return (newtokens, metadata)


class CHAT_SimpleScopedRegex(CHAT_Regex):
    def __init__(self, regex, replacement, scoped, arity):
        self.regex = regex
        self.replacement = replacement
        self.scoped = scoped
        self.arity = arity
        self.compiledre = re.compile(refunction(self.regex))

    def apply(self, tokens, annotation, repkeep):
        newtokens = []
        metadata = []
        todotokens = tokens
        ltodotokens = len(todotokens)
        tokenctr = 0

        # while todotokens != []:
        while tokenctr < ltodotokens:
            scope = findscope(todotokens[tokenctr:], offset=tokenctr)  # this finds a scope part surrounded by <>
            if scope is None:
                # hier misschien iets voor [///] en restart
                newtokens += todotokens[tokenctr:]
                # result = (newtokens, metadata)
                break
            else:
                (b, e) = scope
                if ltodotokens == e + 1:
                    SDLOGGER.error('Scope markings in positions {} and {} not followed by annotation ignored in {}'.format(b, e, show(todotokens)))
                    newtokens += todotokens[:b] + todotokens[b + 1:e]
                    tokenctr = e + 1
                elif self.compiledre.search(todotokens[e + 1].word):
                    annotationwords = [token.word for token in todotokens[b + 1:e]]
                    annotationpositions = [token.pos for token in todotokens[b + 1:e]]
                    if self.arity == dyadic:
                        if ltodotokens <= e + 2:
                            SDLOGGER.error('Missing second argument for dyadic annotation {} in {}'.format(annotation.name, show(todotokens)))
                            newtokens += todotokens[b + 1:e]
                            break
                        else:
                            annotatedwords = [todotokens[e + 2].word] if self.replacement == eps else []
                            annotatedpositions = [todotokens[e + 2].pos] if self.replacement == eps else []
                    elif self.arity == monadic:
                        annotatedwords = []
                        annotatedpositions = []
                    else:
                        SDLOGGER.error('Illegal arity specification ({}) on {}'.format(self.arity, annotation.name))
                        annotatedwords = []
                        annotatedpositions = []
                    newmeta = annotation.metadatafunction(annotation, annotationwords, annotatedpositions, annotatedwords, annotationpositions)
                    metadata.append(newmeta)
                    newtokens += todotokens[tokenctr:b]
                    replacement = getreplacement(repkeep, annotation)
                    newtokens = doreplacement(todotokens[b + 1:e], replacement, newtokens)
                    tokenctr = e + 2
                else:
                    newtokens += todotokens[tokenctr:e + 1]
                    # todotokens = todotokens[e+1:]
                    tokenctr = e + 1

        # the code with a scoped token sequence
        # look for the code
        todotokens = newtokens
        ltodotokens = len(todotokens)
        newtokens = []
        prevtoken = None
        scopewords = []
        scopepositions = []
        i = 0
        while i < ltodotokens:
            if self.compiledre.search(todotokens[i].word):
                if scopewords == []:
                    SDLOGGER.error('First argument of annotation {} missing. Annotation ignored'.format(annotation.name))
                else:
                    if self.arity == monadic:
                        annotatedpositions = []
                        annotatedwords = []
                        replacement = getreplacement(repkeep, annotation)
                        newtokens = doreplacement([prevtoken], replacement, newtokens)
                        prevtoken = None
                        newmeta = annotation.metadatafunction(annotation, scopewords, annotatedpositions,
                                                              annotatedwords, scopepositions)
                        metadata.append(newmeta)
                    elif self.arity == dyadic:
                        if i + 1 >= ltodotokens:
                            SDLOGGER.error('Missing second argument for dyadic annotation {} in {}'.format(annotation.name,
                                                                                                           show(todotokens)))
                        else:
                            annotatedpositions = [todotokens[i + 1].pos]
                            annotatedwords = [todotokens[i + 1].word]
                            replacement = getreplacement(repkeep, annotation)
                            newtokens = doreplacement([prevtoken], replacement, newtokens)
                            prevtoken = None
                            newmeta = annotation.metadatafunction(annotation, scopewords, annotatedpositions, annotatedwords, scopepositions)
                            metadata.append(newmeta)
            else:
                if prevtoken is not None:
                    newtokens.append(prevtoken)
                scopewords = [todotokens[i].word]
                scopepositions = [todotokens[i].pos]
                prevtoken = todotokens[i]

            i += 1
        if prevtoken is not None:
            newtokens.append(prevtoken)
        return (newtokens, metadata)


class CHAT_ComplexRegex(CHAT_Regex):
    def __init__(self, regextuple, replacementtuple, scoped, containswords=False):
        self.regexbegin = regextuple[0]               # 3 elements: begin mid end
        self.regexmid = regextuple[1]               # 3 elements: begin mid end
        self.regexend = regextuple[2]               # 3 elements: begin mid end
        self.scopereplacement = replacementtuple[0]   # 2 elements: one for the scope and one for the text between [ ]
        self.bracketreplacement = replacementtuple[1]   # 2 elements: one for the scope and one for the text between [ ]
        self.scoped = scoped
        self.containswords = containswords
        self.compiledrebegin = re.compile(refunction(self.regexbegin))
        self.compiledremid = re.compile(refunction(self.regexmid))
        self.compiledreend = re.compile(refunction(self.regexend))

    def apply(self, tokens, annotation, repkeep):
        bracketregexes = (self.compiledrebegin, self.compiledremid, self.compiledreend)
        metadata = []
        estates = [bstate, wstate]
        state = bstate
        tokenctr = 0
        todotokens = tokens
        newtokens = []
        tobereplacedtokens = []
        while tokenctr < len(tokens):
            token = todotokens[tokenctr]
            inc = 1
            if state == bstate:
                if token.word == '<':
                    state = scopestate
                elif wordre.search(token.word):
                    state = wstate
                    tobereplacedtokens = [token]
                elif self.compiledrebegin.search(token.word):
                    state = rfoundstate
                else:
                    state = bstate
                    newtokens.append(token)
            elif state == wstate:
                if token.word == '<':
                    newtokens += tobereplacedtokens
                    tobereplacedtokens = []
                    state = scopestate
                elif self.compiledrebegin.search(token.word):
                    state = rfoundstate
                elif wordre.search(token.word):
                    state = wstate
                    newtokens += tobereplacedtokens
                    tobereplacedtokens = [token]
                else:
                    state = wstate
                    newtokens += tobereplacedtokens
                    tobereplacedtokens = [token]
            elif state == scopestate:
                scope = findscope(tokens[tokenctr - 1:], offset=tokenctr - 1)
                if scope is None:
                    SDLOGGER.error('No closing bracket found for < with pos={} in {}'.format(tokens[tokenctr - 1].pos, show(tokens)))
                    state = wstate
                else:
                    (b, e) = scope
                    tobereplacedtokens = todotokens[b:e + 1]
                    state = wstate
                    inc = e - tokenctr + 1
            elif state == rfoundstate:
                bbbe = findbrackets(todotokens[tokenctr - 1:], bracketregexes, offset=tokenctr - 1)
                if bbbe is not None:
                    (bracketbegin, bracketend) = bbbe
                    annotationtokens = todotokens[bracketbegin + 1: bracketend]
                    (cleanannotationtokens, innermetadata) = cleanCHILDEStokens.cleantokens(annotationtokens, repkeep) if self.containswords else (annotationtokens, [])
                    metadata += innermetadata
                    annotatedwords = [t.word for t in tobereplacedtokens if t.word not in ['<', '>']]
                    annotatedpositions = [t.pos for t in tobereplacedtokens if t.word not in ['<', '>']]
                    thevalue = [token.word for token in cleanannotationtokens]
                    annotationpositions = [token.pos for token in cleanannotationtokens]
                    newmeta = annotation.metadatafunction(annotation, thevalue, annotatedpositions, annotatedwords, annotationpositions)
                    metadata.append(newmeta)
                    replacement = self.scopereplacement
                    repltokens = [t for t in tobereplacedtokens if t.word not in ['<', '>']]
                    newtokens = doreplacement(repltokens, replacement, newtokens)
                    if self.bracketreplacement == keep:
                        newtokens += cleanannotationtokens
                    elif self.bracketreplacement == eps:
                        pass
                    else:
                        SDLOGGER.error('Unknown replacementtype: {} in {}'.format(self.scopereplacement, show(tokens)))
                    tobereplacedtokens = []
                    inc = bracketend - bracketbegin
                state = wstate
            tokenctr += inc
        newtokens += tobereplacedtokens
        if state in estates:
            return(newtokens, metadata)
        else:
            SDLOGGER.error('Not in an end state, state={} in {}'.format(state, show(tokens)))
            return(tokens, [])


def findbrackets(tokens, regexes, offset=0):
    (bregex, mregex, eregex) = regexes
    b1e1 = bracketseq(tokens, bregex, mregex, eregex)
    if b1e1 is not None:
        (b1, e1) = b1e1
        result = (b1 + offset, e1 + offset)
    else:
        result = None
    return result


def getsfvalue(w):
    index = w.find('@')
    result = w[index:]
    return result


def getsfword(w):
    index = w.find('@')
    result = w[:index]
    return result


def dropbrackets(w):
    result1 = [c for c in w if c not in ['(', ')']]
    result = eps.join(result1)
    return result


def simplemetafunction(f):
    return lambda ann, pos, w: Meta(ann.name, [f(w)], annotatedposlist=[pos], annotatedwordlist=[w], source=CHAT)


def simplescopedmetafunction(ann, annotationwordlist, annotatedposlist, annotatedwordlist, annotationposlist):
    return Meta(ann.name, annotationwordlist, annotationposlist=annotationposlist, annotatedposlist=annotatedposlist, annotatedwordlist=annotatedwordlist, source=CHAT)


def complexmetafunction(ann, annotationwordlist, annotatedposlist, annotatedwordlist, annotationposlist):
    return Meta(ann.name, annotationwordlist, annotationposlist=annotationposlist, annotatedwordlist=annotatedwordlist, annotatedposlist=annotatedposlist, source=CHAT)


def epsf(w):
    return ''


interposedpat = r'^&\*(\w\w\w:[\w:]+)$'
interposedre = re.compile(interposedpat)


def interposedword(w):
    result1 = interposedre.findall(w)
    result = ''.join(result1)
    return result


def dropinitial(w):
    if w is None:
        result = None
    else:
        result = w[1:]
    return result


def dropzero(w):
    if w is None:
        result = None
    elif w[0] == '0':
        result = w[1:]
    else:
        result = w
    return result


def dropsubstr(w, s):
    if w is None or s is None:
        result = w
    else:
        ls = len(s)
        sindex = w.find(s)
        result = w[:sindex] + w[sindex + ls:]
    return result


def dropchars(c):
    return lambda w: dropchars2(w, c)


def dropchars2(w, c):
    result1 = [ch for ch in w if ch != c]
    result = ''.join(result1)
    return result


def CHAT_message(msg):
    def result(x, y):
        return SDLOGGER.warning(msg.format(x, y))
    return result


annotations = [
    # overlap crucially before annotations taht delete things
    CHAT_Annotation('Overlap Follows', '8.4:71', '10.3:74-75',
                    CHAT_SimpleScopedRegex(r'\[\>[0-9]?\]', keep, True, monadic), simplescopedmetafunction),
    # here additional things could be done
    CHAT_Annotation('Overlap Precedes', '8.4:71-72', '10.3:75',
                    CHAT_SimpleScopedRegex(r'\[\<[0-9]?\]', keep, True, monadic), simplescopedmetafunction),
    CHAT_Annotation('Special Form', '6.3:37', '8.3:43-44', CHAT_SimpleRegex(specialformpat, getsfword, False), simplemetafunction(getsfvalue)),
    CHAT_Annotation('Unintelligible Speech', '6.4:41', '8.4:47', CHAT_SimpleRegex(r'xxx', keep, False), simplemetafunction(epsf)),
    CHAT_Annotation('Phonological Coding', '6.4:41', '8.4:47', CHAT_SimpleRegex(r'yyy', keep, False), simplemetafunction(epsf)),
    CHAT_Annotation('Noncompletion of a Word', '6.5:43', '8.5:48',
                    CHAT_InWordRegex(r'\(([-\w\']*)\)', r'\1'), complexmetafunction),
    CHAT_Annotation('Omitted Word', '6.5:43', '8.5:48-49',
                    CHAT_SimpleRegex(r'0[\w:]+', dropzero, False), simplemetafunction(dropzero)),
    CHAT_Annotation('Satellite at End', '7.4:58', '9.2:59-60',
                    CHAT_SimpleRegex(r'\s„\s', eps, False), simplemetafunction(identity)),
    CHAT_Annotation('Satellite in Beginning', '7.4:58', '9.2:59-60',
                    CHAT_SimpleRegex(r'\s‡\s', eps, False), simplemetafunction(identity)),
    CHAT_Annotation('Falling Tone', '7.6:59', '9.8:63',
                    CHAT_SimpleRegex(u'\u2193', eps, False), simplemetafunction(identity)),
    CHAT_Annotation('Rising Tone', '7.6:59', '9.8:63',
                    CHAT_SimpleRegex(u'\u2191', eps, False), simplemetafunction(identity)),
    CHAT_Annotation('Primary Stress', '7.7:59', '9.9:63', CHAT_InWordRegex(u'\u02C8', ''), complexmetafunction),
    CHAT_Annotation('Secondary Stress', '7.7:59', '9.9:63', CHAT_InWordRegex(u'\u02CC', ''), complexmetafunction),
    CHAT_Annotation('Lengthened Syllable', '7.7:59-60', '9.9:63', CHAT_InWordRegex(r':', ''), complexmetafunction),
    CHAT_Annotation('Blocking', '7.7:60', '9.9:64', CHAT_SimpleRegex(r'\^' + wordpat, dropinitial, False),
                    simplemetafunction(dropinitial)),  # this one must crucially precede Pause Between Syllables
    CHAT_Annotation('Pause Between Syllables', '7.7:60', '9.9:63-64', CHAT_InWordRegex(r'\^', ''), complexmetafunction),
    CHAT_Annotation('Simple Event', '7.8.1:60', '9.10.1:64-65', CHAT_SimpleRegex(r'&=[\w:]+', eps, False),
                                    simplemetafunction(identity)),
    CHAT_Annotation('Complex Local Event', '7.8.2:61', '9.10.3:65', CHAT_ComplexRegex((r'\[\^\s', wordorpuncpat, r'\]'), (keep, eps), False),
                    complexmetafunction),
    CHAT_Annotation('Pause', '7.8.3:62', '9.10.4:66', CHAT_SimpleRegex(r'\(\.\.?\.?\)', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Timed Pause', '7.8.3:62', '9.10.4:66', CHAT_SimpleRegex(r'\([0-9]+\.[0-9]+\)', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Long Event', '7.8.4:62', '9.10.5:66',
                    CHAT_ComplexRegex((r'&{l=[\w:]+', wordpat, r'&}l=[\w:]+'), (keep, eps), True),
                    complexmetafunction),  # no check that the latter part equals the initial part
    CHAT_Annotation('Long Nonverbal Event', '7.8.4:62', '9.10.5:66',
                    CHAT_ComplexRegex((r'&{n=[\w:]+', wordpat, r'&}n=[\w:]+'), (keep, eps), True),
                    complexmetafunction),  # no check that the latter part equals the initial part
    CHAT_Annotation('Trailing Off', '7.9:62', '9.11:66', CHAT_SimpleRegex(r'\+\.\.\.', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Trailing Off of a Question', '7.9:63', '9.11:67', CHAT_SimpleRegex(r'\+\.\.\?', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Question With Exclamation', '7.9:63', '9.11:67', CHAT_SimpleRegex(r'\+!\?', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Interruption', '7.9:63', '9.11:67', CHAT_SimpleRegex(r'\+/\.', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Interruption of a Question', '7.9:63', '9.11:67', CHAT_SimpleRegex(r'\+/\?', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Self-Interruption', '7.9:64', '9.11:68', CHAT_SimpleRegex(r'\+//\.', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Self-Interrupted Question', '7.9:64', '9.11:68', CHAT_SimpleRegex(r'\+//\?', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Transcription Break', '7.9:64', '9.11:68', CHAT_SimpleRegex(r'\+\.', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Quotation Begin', '7.9:64', '9.11:68', CHAT_SimpleRegex(u'\u201C', keep, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Quotation End', '7.9:64', '9.11:68', CHAT_SimpleRegex(u'\u201D', keep, False),
                    simplemetafunction(identity)),
    # CHAT_Annotation('Inner Quotation Begin', '7.9', '64', CHAT_SimpleRegex(u'\u2018', keep, False),
    #                simplemetafunction(identity)), # not anymore in the 2020-06-19 edition
    # CHAT_Annotation('Inner Quotation End', '7.9', '64', CHAT_SimpleRegex(u'\u2019', keep, False),
    #                simplemetafunction(identity)), # not anymore in the 2020-06-19 edition
    CHAT_Annotation('Quotation Follows', '7.9:64-65', '9.11:68-69', CHAT_SimpleRegex(r'\+\"/\.', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Quotation Precedes', '7.9:65', '9.11:69', CHAT_SimpleRegex(r'\+\"\.', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Quoted Utterance', '7.10:65', '9.11:69', CHAT_SimpleRegex(r'\+\"', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Quick Uptake', '7.10:65', '9.11:69', CHAT_SimpleRegex(r'\+\^', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Lazy Overlap', '7.10:65-66', '10.3:75', CHAT_SimpleRegex(r'\+\<', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Self Completion', '7.10:66', '9.11:69', CHAT_SimpleRegex(r'\+,', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Other Completion', '7.10:66', '9.11:69-70', CHAT_SimpleRegex(r'\+\+', eps, False),
                    simplemetafunction(identity)),

    # erroR marking crucially before [/] [//] [///] etc
    CHAT_Annotation('Error Marking', '8.5:75', '10.5:78', CHAT_SimpleScopedRegex(r'\[\*\]', keep, True, monadic),
                    simplescopedmetafunction),
    CHAT_Annotation('Error Marking', '8.5:75', '10.5:78',
                    CHAT_ComplexRegex((r'\[\*', r'[\w:\-\+=]+', r'\]'), (keep, eps), False),
                    complexmetafunction),

    CHAT_Annotation('Pic Bullet', '8.1:67', '10.1:71', CHAT_ComplexRegex((u'\u00b7' + r'%pic:', filenamepat, u'\u00b7'), (keep, eps), True),
                    complexmetafunction),  # pic bullet and text bullet must essentially before time alignment
    CHAT_Annotation('Text Bullet', '8.1:67', '10.1:71', CHAT_ComplexRegex((u'\u00b7' + r'%txt:', filenamepat, u'\u00b7'), (keep, eps), True),
                    complexmetafunction),
    CHAT_Annotation('Time Alignment', '7.10:67', '10.1:71', CHAT_ComplexRegex((u'\u00b7', r'[0-9_]+', u'\u00b7'), (keep, eps), True),
                    complexmetafunction),
    CHAT_Annotation('Time Alignment', '7.10:67', '10.1:71', CHAT_ComplexRegex((u'\u0015', r'[0-9_]+', u'\u0015'), (keep, eps), True),
                    complexmetafunction),  # not an official code but it occurs as such in CLPF
    CHAT_Annotation('Paralinguistic Material', '8.2:68', '10.1:72', CHAT_ComplexRegex((r'\[=!', anybutrb, r'\]'), (keep, eps), True),
                    complexmetafunction),
    CHAT_Annotation('Stressing', '8.2:68', '10.1:72', CHAT_SimpleScopedRegex(r'\[!\]', keep, False, monadic),
                    simplescopedmetafunction),
    CHAT_Annotation('Contrastive Stressing', '8.2:68', '10.1:72', CHAT_SimpleScopedRegex(r'\[!!\]', keep, False, monadic),
                    simplescopedmetafunction),
    # Duration to be added here @@
    CHAT_Annotation('Explanation', '8.3:69', '10.3:73', CHAT_ComplexRegex((r'\[=', anybutrb, r'\]'), (keep, eps), False),
                    complexmetafunction),
    CHAT_Annotation('Replacement', '8.3:69', '10.3:73',
                    CHAT_ComplexRegex((r'\[:\s', r'([^\]]+)', r'\]'), (eps, keep), True, containswords=True), complexmetafunction),
    CHAT_Annotation('Replacement of Real Word', '8.3:70', '10.3:73',
                    CHAT_ComplexRegex((r'\[::', r'([^\]]+)', r'\]'), (eps, keep), True), complexmetafunction),
    CHAT_Annotation('Alternative Transcription', '8.3:70', '10.3:74',
                    CHAT_ComplexRegex((r'\[=\?', r'([^\]]+)', r'\]'), (keep, eps), True), complexmetafunction),
    CHAT_Annotation('Dependent Tier on Main Line', '8.3:70', 'none',
                    CHAT_ComplexRegex((r'\[%\w\w\w:', anybutrb, r'\]'), (keep, eps), True), complexmetafunction),  # @@must do something with the speaker
    CHAT_Annotation('Comment on Main Line', '8.3:70', '10.3:74',
                    CHAT_ComplexRegex((r'\[%\s+', anybutrb, r'\]'), (keep, eps), True), complexmetafunction),
    CHAT_Annotation('Best Guess', '8.3:70-71', '10.3:74', CHAT_SimpleScopedRegex(r'\[\?\]', keep, True, monadic), simplescopedmetafunction),
    CHAT_Annotation('Repetition', '8.4:72', '10.4:75-76', CHAT_SimpleScopedRegex(r'\[/\]', eps, True, monadic), simplescopedmetafunction),
    CHAT_Annotation('Multiple Repetition', '8.4:72-73', '10.4:76',
                    CHAT_ComplexRegex((r'\[x', r'[0-9]+', r'\]'), (keep, eps), True), complexmetafunction),
    CHAT_Annotation('Retracing', '8.4:73', '10.4:76-77', CHAT_SimpleScopedRegex(r'\[//\]', eps, True, monadic), simplescopedmetafunction),
    CHAT_Annotation('Reformulation', '8.4:73-74', '10.4:77', CHAT_SimpleScopedRegex(r'\[///\]', eps, True, monadic), simplescopedmetafunction),
    CHAT_Annotation('False Start Without Retracing', '8.4:74', '10.4:77', CHAT_SimpleScopedRegex(r'\[/\-\]', eps, True, dyadic), simplescopedmetafunction),
    CHAT_Annotation('Unclear Retracing Type', '8.4:74', '10.4:77', CHAT_SimpleScopedRegex(r'\[/\?\]', keep, True, monadic), simplescopedmetafunction),
    CHAT_Annotation('Excluded Material', '', '10.4:77-78', CHAT_SimpleScopedRegex(r'\[e\]', eps, True, monadic), simplescopedmetafunction),
    CHAT_Annotation('Clause Delimiter', '8.4:74', '78', CHAT_SimpleRegex(r'\[\^c\]', eps, False), simplemetafunction(identity)),    # needs extension
    CHAT_Annotation('Interposed Word', '8.4:74', '9.10.2:65', CHAT_SimpleRegex(r'&\*\w\w\w:[\w:]+', eps, False),  # grouped metadata would come in handy here ID100 text speaker = XXX, ID100 text interposedword = hmm
                    simplemetafunction(interposedword)),
    CHAT_Annotation('Postcode', '8.6:75', '10.5:78', CHAT_ComplexRegex((r'\[\+\s+', wordpat, r'\]'), (keep, eps), False),
                    complexmetafunction),
    CHAT_Annotation('Language Precode', '8.6:75', '10.5:79', CHAT_ComplexRegex((r'\[\-\s+', wordpat, r'\]'), (keep, eps), False),
                    complexmetafunction),
    CHAT_Annotation('Excluded Utterance', '8.6:75-76', '10.5:79', CHAT_SimpleRegex(r'\[\+\s+bch\]', eps, False),
                    simplemetafunction(interposedword)),
    CHAT_Annotation('Included Utterance', '8.6:76', '10.5:79', CHAT_SimpleRegex(r'\[\+\s+trn\]', eps, False),
                    simplemetafunction(interposedword)),
    CHAT_Annotation('Zero Utterance', '', '10.5:79, 11.1:81', CHAT_SimpleRegex(r'\b0\b', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('Segment Repetition', '10:85,11:89', '13:91', CHAT_InWordRegex(u'\u21AB.*?\u21AB', ''), complexmetafunction),
    CHAT_Annotation('Joined Words', '6.6.4:46', '8.6.3:51', CHAT_InWordRegex(r'_', space), complexmetafunction),  # take care extra token!@@
    CHAT_Annotation('Clitic Boundary', '6.6.15:52', 'not found', CHAT_InWordRegex(r'~', space), complexmetafunction),  # take care extra token@@
    CHAT_Annotation('Blocked Segments', '10:85,11:89', '13:91', CHAT_InWordRegex(u'\u2260.*?\u2260', ''),
                    complexmetafunction),
    # these must be applied after [/], [//], [///] etc
    CHAT_Annotation('Untranscribed Material', '6.4:42', '8.4:47', CHAT_SimpleRegex(r'www', eps, False),
                    simplemetafunction(epsf)),
    CHAT_Annotation('Phonological Fragment', '6.4:42', '8.4:48',
                    CHAT_SimpleRegex(r'&' + simplewordpat, eps, False), simplemetafunction(identity)),
    CHAT_Annotation('Phonological Fragment', 'None', '8.4:48; https://talkbank.org/manuals/Clin-CLAN.pdf '
                                                     'states &+ for phonological fragments(p. 18)',
                    CHAT_SimpleRegex(r'&\+' + simplewordpat, eps, False), simplemetafunction(identity)),
    CHAT_Annotation('Filler', 'None', '8.4:48',
                    CHAT_SimpleRegex(r'&\-' + wordpat, eps, False), simplemetafunction(identity)),

    # ad-hoc extensiosn for Lotti
    CHAT_Annotation('[een]', 'ad-hoc extension', 'ad-hoc extension', CHAT_SimpleRegex(r'\[een\]', eps, False),
                    simplemetafunction(identity)),
    CHAT_Annotation('[twee]', 'ad-hoc extension', 'ad-hoc extension', CHAT_SimpleRegex(r'\[twee\]', eps, False),
                    simplemetafunction(identity)),

]


def findscope(tokenlist, offset=0):
    bregex = re.compile(r'^\<$')
    mregex = re.compile(r'^[^\<\>]+$')
    eregex = re.compile(r'^\>$')
    result1 = bracketseq(tokenlist, bregex, mregex, eregex)
    if result1 is None:
        result = None
    else:
        (b, e) = result1
        result = (b + offset, e + offset)
    return result


def bracketseq(tokenlist, bregex, mregex, eregex):
    state = bstate
    tokenctr = 0
    if tokenlist is None:
        return None
    for token in tokenlist:
        if state == bstate:
            if bregex.search(token.word):
                begin = tokenctr
                state = mstate
            else:
                pass
        elif state == mstate:
            if eregex.search(token.word) is not None:
                end = tokenctr
                state = estate
            elif bregex.search(token.word) is not None:
                SDLOGGER.error('Range Open symbol encountered inside brackets in {}'.format(show(tokenlist)))
                state = mstate
            elif mregex.search(token.word) is not None:
                state = mstate
            else:
                SDLOGGER.error('Incorrect element between brackets ({}) in: {}'.format(token.word, show(tokenlist)))
                state = mstate
        elif state == estate:
            break
        tokenctr += 1
    if state == estate:
        result = (begin, end)
    else:
        result = None
    return result


def anysearch(reset, word):
    result = False
    for regex in reset:
        if result:
            return result
        else:
            if regex.search(word):
                result = True
    return result


def isopenbracket(word):
    result = anysearch(openbrackets, word)
    return result


def isclosebracket(word):
    result = anysearch(closebrackets, word)
    return result


def get_CHATpatterns(annotations):
    result = set()
    # include scope begin and end
    result = result.union({r'\<', r'\>'})
    openbrackets = set()
    closebrackets = set()
    # include regular expressions from the annotations
    for annotation in annotations:
        newpats = set()
        theregex = annotation.regex
        if isinstance(theregex, CHAT_SimpleRegex):
            newpats = {theregex.regex}
        elif isinstance(theregex, CHAT_SimpleScopedRegex):
            newpats = {theregex.regex}
        elif isinstance(theregex, CHAT_ComplexRegex):
            newpats = {theregex.regexbegin, theregex.regexend}
            openbrackets = openbrackets.union({theregex.compiledrebegin})
            closebrackets = closebrackets.union({theregex.compiledreend})
        elif isinstance(theregex, CHAT_InWordRegex):
            newpats = {}
        else:
            SDLOGGER.error('Unknown Regex type: {}'.format(theregex))
            newpats = {}
        result = result.union(newpats)
    return (result, openbrackets, closebrackets)


(CHAT_patterns, openbrackets, closebrackets) = get_CHATpatterns(annotations)
