import re

vertbar = '|'
space = ' '
hyphen = '-'
slash = '/'
tab = '\t'
comma = ','

wpat = r'^.*\w.*$'
wre = re.compile(wpat)
allhyphenspat = r'^-+$'
allhyphensre = re.compile(allhyphenspat)

barevowels = 'aeiouy'
aiguvowels = 'áéíóúý'
gravevowels = 'àèìòù\u00FD'
tremavowels = 'äëïöüÿ'
circumflexvowels = 'âêîôû\u0177'


consonants = 'bcdfghjklmnpqrstvwxz\u00E7'  # \u00E7 is c cedilla
dutch_base_vowels = barevowels + aiguvowels + gravevowels + tremavowels + circumflexvowels
vowels = dutch_base_vowels
dutch_base_diphthongs = ['aa', 'ee', 'ie', 'oo', 'uu', 'ij', 'ei', 'au', 'ou', 'ui', 'eu', 'oe']
dutch_y_diphthongs = ['y' + d for d in dutch_base_vowels] + [d + 'y' for d in dutch_base_vowels]  # ryen gaat nog fout ye alleen samen nemen aan begin van woord
dutch_y_triphthongs = ['y' + d for d in dutch_base_diphthongs] + [d + 'y' for d in dutch_base_diphthongs]
dutch_trema_diphthongs = ['äa', "ëe", 'ïe', 'öo', 'üu', 'ëi']
dutch_diphthongs = dutch_base_diphthongs + dutch_y_diphthongs + dutch_trema_diphthongs
dutch_base_triphthongs = ['aai', 'eeu', 'ooi', 'oei']
dutch_y_tetraphthongs = ['y' + d for d in dutch_base_triphthongs]
dutch_triphthongs = dutch_base_triphthongs + dutch_y_triphthongs
dutch_tetraphthongs = dutch_y_tetraphthongs

hyphenprefixes = ['ex']

singlehyphenpat = r'(^[^-]+)-([^-]+)$'
singlehyphenre = re.compile(singlehyphenpat)

duppattern = r'(.)\1{2,}'
dupre = re.compile(duppattern)


def pad(wrd, i, c=space):
    if len(wrd) > i:
        result = wrd
    else:
        result = wrd.rjust(i, c)
    return result


def star(str):
    return '({})*'.format(str)


def alt(strlist, grouped=True):
    alts = '|'.join(strlist)
    if grouped:
        result = '({})'.format(alts)
    else:
        result = '{}'.format(alts)
    return result


def charrange(string):
    return '[{}]'.format(string)


consonants_star = star(charrange(consonants))

syllableheadspat = alt([alt(dutch_tetraphthongs), alt(dutch_triphthongs), alt(dutch_diphthongs), alt(vowels)])
syllableheadsre = re.compile(syllableheadspat)

monosyllabicpat = r'^' + consonants_star + syllableheadspat + consonants_star + r'$'
monosyllabicre = re.compile(monosyllabicpat)


def barededup(word):
    result = dupre.sub(r'\1', word)
    return result


def deduplicate(word, inlexicon):
    newwords = []
    if wre.match(word):  # we want to exclude tokens consisting of interpunction symbols only e.g  ---, --
        newword = dupre.sub(r'\1', word)
        if inlexicon(newword):
            newwords.append(newword)
        newword = dupre.sub(r'\1\1', word)
        if inlexicon(newword):
            newwords.append(newword)
    return newwords


def fullworddehyphenate(word, inlexicon):
    newtokens = []
    newwords = dehyphenate(word)
    newwordset = set(newwords)
    for newword in newwordset:
        if inlexicon(newword):
            newtokens.append(newword)
    if newtokens == []:
        newwords = delhyphenprefix(word, inlexicon)
        newwordset = set(newwords)
        for newword in newwordset:
            newtokens.append(newword)
    return newtokens


def delhyphenprefix(word, inlexicon):
    m = singlehyphenre.match(word)
    if m is not None:
        prefix = m.group(1)
        mainword = m.group(2)
        mwinlex = inlexicon(mainword)
        pfinlex = inlexicon(prefix)
        deduppf = barededup(word)
        if prefix in hyphenprefixes and mwinlex:       # the word starts wit ha known prefix that uses hyphen such as ex (ex-vrouw)
            result = []
        elif mainword.startswith(prefix) and mwinlex:  # this is the core case  e.g. ver-verkoop
            result = [mainword]
        elif pfinlex and mwinlex:                       # for compounds with a hyphen: kat-oorbellen, generaal-majoor and for tennis-baan(?)
            result = []
        elif mainword.startswith(deduppf) and mwinlex:   # vver-verkoop
            result = [mainword]
        else:
            result = []
    else:
        result = []
    return result


def allhyphens(word):
    result = allhyphensre.match(word)
    return result


def dehyphenate(word):
    results = []
    if len(word) == 0:
        results = ['']
    elif allhyphens(word):
        results = [word]
    else:
        head = word[0:1]
        tail = word[1:]
        if head == hyphen:
            # newresult = head + tail
            # results.append(newresult)
            rightresults = dehyphenate(tail)
            for rightresult in rightresults:
                newresult = head + rightresult
                results.append(newresult)
                newresult = rightresult
                results.append(newresult)
        else:
            tailresults = dehyphenate(tail)
            for tailresult in tailresults:
                newresult = head + tailresult
                results.append(newresult)
    return results


def isconsonant(char):
    if len(char) != 1:
        result = False
    elif char.lower() in consonants:
        result = True
    else:
        result = False
    return result


def isvowel(char):
    if len(char) != 1:
        result = False
    elif char.lower() in vowels:
        result = True
    else:
        result = False
    return result


def endsinschwa(word):
    # Ce of Vie of ije or ë
    if word[-3:] == 'ije':
        result = True
    elif word[-2:] == 'ie' and isvowel(word[-3:-2]):
        result = True
    elif word[-1:] == "ë":
        result = True
    elif word[-1:] == 'e' and isconsonant(word[-2:-1]):
        result = True
    else:
        result = False
    return result


def isdiphthong(d):
    result = d in dutch_diphthongs
    return result


def istriphthong(d):
    result = d in dutch_triphthongs
    return result


def monosyllabic(word):
    result = monosyllabicre.match(word)
    return result


def accentaigu(word):
    if len(word) == 0:
        results = []
    elif isvowel(word[0]):
        restresults = accentaigu(word[1:])
        results1 = [word[0] + wrest for wrest in restresults]
        results2 = [aigu(word[0]) + wrest for wrest in restresults]
        results = results1 + results2
    return results


def aigu(c):
    theindex = barevowels.find(c)
    result = aiguvowels[theindex]
    # TODO: Check this return
    return result


def nono(inval):
    result = (inval is None) or (inval == 0) or (inval == []) or (inval == '')
    return result


def nonnull(inval):
    result = not(nono(inval))
    return result


def allconsonants(inval):
    result = all([isconsonant(c) for c in inval])
    return result


def string2list(liststr):
    if liststr is None or len(liststr == 1):
        return []
    elif liststr[0] == '[' and liststr[-1] == ']':
        core = liststr[1:-1]
        parts = core.split(comma)
        return parts
