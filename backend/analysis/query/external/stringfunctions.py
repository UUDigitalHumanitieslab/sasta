import re

vertbar = '|'
space = ' '
hyphen = '-'
slash = '/'
tab = '\t'


barevowels = 'aeiouy'
aiguvowels = 'áéíóúý'
gravevowels = 'àèìòù\u00FD'
tremavowels = 'äëïöüÿ'
circumflexvowels = 'âêîôû\u0177'


consonants = 'bcdfghjklmnpqrstvwxz\u00E7'  # \u00E7 is c cedilla
dutch_base_vowels = barevowels + aiguvowels + \
    gravevowels + tremavowels + circumflexvowels
vowels = dutch_base_vowels
dutch_base_diphthongs = ['aa', 'ee', 'ie', 'oo',
                         'uu', 'ij', 'ei', 'au', 'ou', 'ui', 'eu', 'oe']
# ryen gaat nog fout ye alleen samen nemen aan begin van woord
dutch_y_diphthongs = ['y' + d for d in dutch_base_vowels] + \
    [d + 'y' for d in dutch_base_vowels]
dutch_y_triphthongs = ['y' + d for d in dutch_base_diphthongs] + \
    [d + 'y' for d in dutch_base_diphthongs]
dutch_trema_diphthongs = ['äa', "ëe", 'ïe', 'öo', 'üu', 'ëi']
dutch_diphthongs = dutch_base_diphthongs + \
    dutch_y_diphthongs + dutch_trema_diphthongs
dutch_base_triphthongs = ['aai', 'eeu',  'ooi',   'oei']
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

syllableheadspat = alt([alt(dutch_tetraphthongs), alt(
    dutch_triphthongs), alt(dutch_diphthongs), alt(vowels)])
syllableheadsre = re.compile(syllableheadspat)

monosyllabicpat = r'^' + consonants_star + \
    syllableheadspat + consonants_star + r'$'
monosyllabicre = re.compile(monosyllabicpat)


def deduplicate(word, inlexicon):
    newwords = []
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
            if inlexicon(newword):
                newtokens.append(newword)
    return newtokens


def delhyphenprefix(word, inlexicon):
    m = singlehyphenre.match(word)
    if m is not None:
        prefix = m.group(1)
        mainword = m.group(2)
        if prefix in hyphenprefixes and inlexicon(mainword):
            result = [word]
        else:
            result = [singlehyphenre.sub(r'\2', word)]
    else:
        result = []
    return result


def dehyphenate(word):
    results = []
    if len(word) == 0:
        results = ['']
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
    return result


def testcondition(condition, word):
    if condition(word):
        print('OK:{}'.format(word))
    else:
        print('NO:{}'.format(word))


def test():
    monosyllabicwords = ['baai', 'eeuw', 'mooi', 'aap',   'deed', 'Piet', 'noot', 'duut', 'rijd', 'meid', 'rauw', 'koud', 'buit', 'reuk', 'boer', 'la', 'de', 'hik', 'dop', 'dut',
                         'yell', 'ry', 'Händl', 'Pëtr', 'bït', 'Köln',  'Kür', 'Tÿd']
    disyllabicwords = ['baaien', 'eeuwen', 'mooie', 'aapje',   'deden', 'Pietje', 'noten', 'dut', 'rijden', 'meiden', 'rauwe', 'koude', 'buitje', 'reuken', 'boeren', 'laden', 'dender',
                       'hikken', 'doppen', 'dutten', 'yellen', 'ryen', 'Händler', 'Pëtri', 'bïty', 'Kölner',  'Kürer', 'Tÿding', 'naäap', 'meeëten', 'ciën', 'coöp']

    for word in monosyllabicwords:
        testcondition(monosyllabic, word.lower())
    for word in disyllabicwords:
        testcondition(monosyllabic, word.lower())

    for word in monosyllabicwords + disyllabicwords:
        ms = syllableheadsre.finditer(word)
        print(word, end=' -- ')
        for m in ms:
            print(m.group(0), end=', ')
        print('')


if __name__ == '__main__':
    test()
