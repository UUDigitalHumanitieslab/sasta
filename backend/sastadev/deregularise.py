import csv
import re
import os
from sastadev import SD_DIR

tab = '\t'
plussym = '+'

# maybe also add a variant with e- as prefix instead of ge-, and also without ge-


overgen = 'Overgeneralisation'
noge = 'Lacking ge prefix'
nog = 'Prefix ge without onset'
wrongovergen = 'Wrong Overgeneralisation'
wrongen = 'Wrong -en suffix'
nolabel = 'Correct'

metaarr = {}
metaarr['ge'] = ''
metaarr[''] = noge
metaarr['e'] = nog

correctionfilename = 'inflectioncorrection.tsv.txt'

v_prefixes = ['her', 'ver', 'ont']
separable_prefixes = ['aan', 'aaneen', 'aantoe', 'achter', 'achteraan', 'achterna', 'achterom', 'achterop', 'achterover', 'achteruit',
                      'adem', 'ader', 'af', 'auto', 'bakzeil', 'beet', 'bekend', 'belang', 'bellen', 'betreft',
                      'bezig', 'bij', 'bijeen', 'binnen', 'blijk', 'bloot', 'boek', 'bot', 'boven', 'buiten', 'buitenom', 'daar',
                      'dank', 'deel', 'dicht', 'dienst', 'diep', 'dol', 'dood', 'door', 'droog', 'dubbel', 'dwars', 'eruit',
                      'feest', 'fijn', 'flauw', 'gade', 'garant', 'geheim', 'gelijk', 'geluk', 'gelukkig', 'gereed', 'gering', 'gerust',
                      'gevaar', 'gevangen', 'gewaar', 'geweld', 'glad', 'goed', 'groot', 'hard', 'heen', 'heet', 'heruit', 'hoog', 'in',
                      'ineen', 'ja', 'kaal', 'kaart', 'kapot', 'kennis', 'klaar', 'klein', 'komedie', 'kopje', 'kort', 'krom', 'kuit',
                      'kwaad', 'kwijt', 'lam', 'langs', 'ledig', 'leeg', 'les', 'lief', 'los', 'maat', 'mat', 'mede', 'mee', 'mis', 'model',
                      'mooi', 'na', 'nabij', 'nat', 'neder', 'neer', 'om', 'omhoog', 'omlaag', 'omver', 'onder', 'onderdoor', 'onderuit', 'op',
                      'opeen', 'open', 'over', 'overeen', 'overhoop', 'paard', 'paardje', 'plaats', 'plat', 'post', 'prijs', 'raak', 'recht',
                      'rond', 'samen', 'schaak', 'schadeloos', 'scheef', 'school', 'schoon', 'schoot', 'schuil', 'snor', 'stand', 'steek',
                      'stijf', 'stil', 'stop', 'storm', 'stuk', 'tegemoet', 'tegen', 'tegenover', 'tekeer', 'tekort', 'teleur', 'teloor',
                      'teniet', 'tentoon', 'terecht', 'terneder', 'terneer', 'terug', 'tevreden', 'teweeg', 'tewerk', 'thee', 'thuis', 'tijd', 'toe',
                      'toegang', 'toneel', 'tussen', 'uit', 'uiteen', 'up', 'vaarwel', 'vandaan', 'vanzelf', 'vast', 'veil', 'ver', 'verbeurd',
                      'vet', 'vol', 'voor', 'vooraf', 'voorbij', 'voorop', 'voort', 'vooruit', 'vreemd', 'vrij', 'vuil', 'waar', 'wacht',
                      'warm', 'weder', 'weer', 'weerom', 'weg', 'wel', 'wijs', 'zaak', 'zoek', 'zwart']


sorted_separable_prefixes = sorted(separable_prefixes, key=lambda x: len(x))


def correctinflection(word):
    result = getcorrections(word, correction)
    return result


def alt(thestr):
    result = '[' + thestr + ']'
    return result


def plus(thestr):
    result = thestr + '+'
    return result


consonants = 'bcdfghjklmnpqrstvwxz'
vowels = 'aeiouyáéíóúýäëïöüÿàèìòù'
nodiavowels = 'aeiouy'
tremavowels = 'äëïöüÿ'
diphtongs = ['au', 'ei', 'ie', 'ij', 'oe', 'ou', 'ui']
vccvpattern = alt(vowels) + plus(alt(consonants)) + alt(vowels)
vccvre = re.compile(vccvpattern)
tkofschip = ['t', 'k', 'o', 'f', 's', 'ch', 'p', 'sh', 'sj']


def addtrema(vowel):
    ind = nodiavowels.find(vowel)
    if ind >= 0:
        result = tremavowels[ind]
    else:
        result = vowel
    return result


def gendepref(word, prefixes):
    results = []
    result = None
    for sep in prefixes:
        if word.startswith(sep):
            lsep = len(sep)
            base = word[lsep:]
            result = (sep, base)
            results.append(result)
    result = ('', word)
    results.append(result)
    return results


def desep(word, correction):
    results = []
    results1 = gendepref(word, sorted_separable_prefixes)
    for (prefix, base) in results1:
        if base in correction:
            results.append((prefix, '', base))
            results2 = gendepref(base, v_prefixes)
            for (prefix2, base2) in results2:
                if base2 in correction:
                    results.append((prefix, prefix2, base2))
    return results


def finaldegemination(thestr):
    if len(thestr) >= 2 and thestr[-1] == thestr[-2]:
        result = thestr[:-1]
    else:
        result = thestr
    return result


def multiplesyllables(stem):
    match = vccvre.search(stem)
    result = match is not None
    return result


def isConsonant(thechar):
    if len(thechar) != 1:
        result = False
    else:
        result = thechar in consonants
    return result


def isVowel(thechar):
    if len(thechar) != 1:
        result = False
    else:
        result = thechar in vowels
    return result


def isDiphthong(thestr):
    result = len(thestr) == 2 and thestr in diphtongs
    return result


def isVowelGeminate(thestr):
    if len(thestr) != 2:
        result = False
    else:
        result = isDiphthong(thestr) or (isVowel(thestr[1]) and thestr[0] == thestr[1])
    return result


def IJ(thestr):
    result = thestr[-2:] == 'ij'
    return


def ViViC(thestr):
    result = len(thestr) >= 3 and isConsonant(thestr[-1]) and isVowel(thestr[-2]) and thestr[-3] == thestr[-2]
    return result


def VVC(thestr):
    result = len(thestr) >= 3 and isConsonant(thestr[-1]) and isVowelGeminate(thestr[-3:-1])
    return result


def VC1C2(thestr):
    result = len(thestr) >= 3 and isConsonant(thestr[-1]) and isConsonant(thestr[-2]) and thestr[-1] != thestr[-2]
    return result


def VC1C1(thestr):
    result = len(thestr) >= 3 and isConsonant(thestr[-1]) and isConsonant(thestr[-2]) and thestr[-1] == thestr[-2]
    return result


def CVC(thestr):
    result1 = len(thestr) >= 3 and isConsonant(thestr[-1]) and isVowel(thestr[-2]) and isConsonant(thestr[-3])
    result2 = len(thestr) == 2 and isConsonant(thestr[-1]) and isVowel(thestr[-2])  # eten
    result = result1 or result2
    return result


def CV(thestr):
    result = len(thestr) >= 2 and isConsonant(thestr[-2]) and isVowel(thestr[-1])
    return result


def dup(thestr):
    return(thestr + thestr)


def endsin(stem, thechar):
    return(stem[-1] == thechar)


def startswithprefix(stem):
    result1 = len(stem) >= 2 and stem[0:2] in ['be', 'ge'] and multiplesyllables(stem)
    result2 = len(stem) >= 3 and stem[0:3] in v_prefixes and multiplesyllables(stem)
    result = result1 or result2
    return result


def makepastsg(stem, stemFS):
    if stem[-1] in tkofschip or stem[-2:-1] in tkofschip:
        result = stemFS + 'te'
    else:
        result = stemFS + 'de'

    return result, overgen


def makepastpl(stem, stemFS):
    form, meta = makepastsg(stem, stemFS)
    result = form + 'n'
    return result, meta


def makepastpart(stem, stemFS, takesge, prefix='ge'):
    metalabel = overgen
    if stem[-1] in tkofschip or stem[-2:-1] in tkofschip:
        result = stemFS + 't'
    elif CV(stem):
        result = stem + stem[-1] + 'd'
    else:
        result = stemFS + 'd'
    if takesge:
        result = prefix + result
    # no verbs starting with vowel that we must take into account

    if takesge:
        metalabel = plussym.join([metalabel, metaarr[prefix]])

    result = finaldegemination(result)
    return result, metalabel


def makewrongenpastpart(stem, stemFS, takesge, prefix='ge'):
    if ViViC(stemFS):  # maak -> gemaken
        result = stemFS[:-2] + stemFS[-1] + 'en'
    elif CVC(stemFS):   # lik -> gelikken
        result = stemFS + stemFS[-1:] + 'en'
    elif len(stemFS) >= 2 and isDiphthong(stemFS[-2:]):    # doe -> gedoen, zij -> gezijn, but not ei eu?  @@!
        result = stemFS + 'n'
    elif len(stemFS) >= 2 and isConsonant(stemFS[-2]) and isVowel(stemFS[-1]):  # ga -> gegaan
        result = stemFS + stemFS[-1] + 'n'
    else:  # kijk -> gekijken
        result = stemFS + 'en'
    if takesge:
        if prefix == '':
            adaptedresult = result
        elif result[0] in vowels:  # verbs starting with vowel that we must take into account; Yes eten: geëet!
            adaptedresult = addtrema(result[0]) + result[1:]
        else:
            adaptedresult = result
        result = prefix + adaptedresult
    return result, wrongen


def makewrongpastpart(stem, stemFS, takesge, prefix='ge'):
    metalabel = wrongovergen
    if stem[-1] in tkofschip or stem[-2:] in tkofschip:
        result = stemFS + 't'
    elif CV(stem):
        result = stem + stem[-1] + 't'
    elif stem[-1] not in 'd':
        result = stemFS + 't'
    else:
        result = stemFS + 'd'
    if takesge:
        if prefix == '':
            adaptedresult = result
        elif result[0] in vowels:  # verbs starting with vowel that we must take into account; Yes eten: geëet!
            adaptedresult = addtrema(result[0]) + result[1:]
        else:
            adaptedresult = result
        result = prefix + adaptedresult
    result = finaldegemination(result)
    if takesge:
        metalabel = plussym.join([metalabel, metaarr[prefix]])
    return result, overgen


def getcorrections(thestr, correction):
    results = []
    if thestr in correction:
        result = correction[thestr]
        results.append(result)
    else:
        sepresults = desep(thestr, correction)
        for (sep, pref, base) in sepresults:
            if pref + base in correction:
                basestr, meta = correction[pref + base]
                result = sep + basestr, meta  # voor bijv. uitgeloopt
                results.append(result)
            elif base in correction:    # voor bijv uitverloofd,
                basestr, meta = correction[base]
                result = sep + pref + basestr, meta
                results.append(result)
            else:
                geroot = 'ge' + base
                if geroot in correction:
                    basestr, meta = correction[geroot[2:]]
                    result = sep + pref + basestr, meta
                    results.append(result)
                else:
                    result = thestr, nolabel
                    results.append(result)
    results = [(wstr.strip(), meta) for wstr, meta in results]
    return results


def getstems(el):
    base = el[:-2]
    if el[-3:] == 'aan':  # gaan, slaan , staan
        stem = el[:-2]
    elif el[-3:] == 'oen':  # doen
        stem = el[:-1]
    elif el[-3:] == 'ijn':  # zijn
        stem = el[:-1]
    elif IJ(base):  # vrijen
        stem = base
    elif VVC(base):       # gieten
        stem = base
    elif VC1C2(base):   # drinken
        stem = base
    elif VC1C1(base):  # bakken
        stem = el[:-3]
    elif CVC(base):     # dragen
        stem = base[:-2] + dup(base[-2:-1]) + base[-1:]
    else:
        stem = 'niet voorzien: ' + el
    if endsin(stem, 'v'):
        stemFS = stem[:-1] + 'f'
    elif endsin(stem, 'z'):
        stemFS = stem[:-1] + 's'
    else:
        stemFS = stem

    if startswithprefix(stem):
        takesge = False
    else:
        takesge = True
    return(stem, stemFS, takesge)


def makepastpartwithe(stem, stemFS, takesge, prefix='ge'):
    pastpart, metalabel = makepastpart(stem, stemFS, takesge, prefix)
    if pastpart[-2:] == 'en':
        result = pastpart
    elif ViViC(pastpart):   # geloot -> gelote
        result = pastpart[:-3] + pastpart[-2:] + 'e'
    elif CVC(pastpart):  # gelet -> gelette
        result = pastpart + pastpart[-1] + 'e'
    else:
        result = pastpart + 'e'
    return result, metalabel


def makeparadigm(word, forms):

    goodpastsg = forms[word][1]
    goodpastpl = forms[word][2]
    goodpastpart = forms[word][3]
    goodpastpartwithe = goodpastpart + 'e'

    (stem, stemFS, takesge) = getstems(word)

    triples = []

    regularpastsg, metalabel = makepastsg(stem, stemFS)
    triples.append((regularpastsg, metalabel, goodpastsg))

    regularpastpl, metalabel = makepastpl(stem, stemFS)
    triples.append((regularpastpl, metalabel, goodpastpl))

    # perfect participles
    pastparticiple, metalabel = makepastpart(stem, stemFS, takesge)
    triples.append((pastparticiple, metalabel, goodpastpart))

    epastparticiple, metalabel = makepastpart(stem, stemFS, takesge, prefix='e')
    triples.append((epastparticiple, metalabel, goodpastpart))

    zeropastparticiple, metalabel = makepastpart(stem, stemFS, takesge, prefix='')
    triples.append((zeropastparticiple, metalabel, goodpastpart))

    # perfect participle with e
    pastpartwithe, metalabel = makepastpartwithe(stem, stemFS, takesge)
    triples.append((pastpartwithe, metalabel, goodpastpartwithe))

    epastpartwithe, metalabel = makepastpartwithe(stem, stemFS, takesge, prefix='e')
    triples.append((epastpartwithe, metalabel, goodpastpartwithe))

    zeropastpartwithe, metalabel = makepastpartwithe(stem, stemFS, takesge, prefix='')
    triples.append((zeropastpartwithe, metalabel, goodpastpartwithe))

    # perfect participle misspelled t ipv d gevalt
    wrongpastpart, metalabel = makewrongpastpart(stem, stemFS, takesge)
    triples.append((wrongpastpart, metalabel, goodpastpart))

    ewrongpastpart, metalabel = makewrongpastpart(stem, stemFS, takesge, prefix='e')
    triples.append((ewrongpastpart, metalabel, goodpastpart))

    zerowrongpastpart, metalabel = makewrongpastpart(stem, stemFS, takesge, prefix='')
    triples.append((zerowrongpastpart, metalabel, goodpastpart))

    wrongenpastpart, metalabel = makewrongenpastpart(stem, stemFS, takesge)
    triples.append((wrongenpastpart, metalabel, goodpastpart))

    ewrongenpastpart, metalabel = makewrongenpastpart(stem, stemFS, takesge, prefix='e')
    triples.append((ewrongenpastpart, metalabel, goodpastpart))

    zerowrongenpastpart, metalabel = makewrongenpastpart(stem, stemFS, takesge, prefix='')
    triples.append((zerowrongenpastpart, metalabel, goodpastpart))

    if goodpastpart[-2:] == 'en':
        (ppstem, ppstemFS, takesge) = getstems(goodpastpart)
        wrongpastpart2, metalabel = makepastpart(ppstem, ppstemFS, takesge)
        wrongpastpart2a, metalabel = makewrongpastpart(ppstem, ppstemFS, takesge)

    else:
        wrongpastpart2, metalabel = goodpastpart, nolabel
        wrongpastpart2a, metalabel = goodpastpart, nolabel

    triples.append((wrongpastpart2, metalabel, goodpastpart))
    triples.append((wrongpastpart2a, metalabel, goodpastpart))

    egoodpastpart, metalabel = (goodpastpart[1:], nog) if goodpastpart[:2] == 'ge' else (goodpastpart, nolabel)
    triples.append((egoodpastpart, metalabel, goodpastpart))
    zerogoodpastpart, metalabel = (goodpastpart[2:], noge) if goodpastpart[:2] == 'ge' else (goodpastpart, nolabel)
    triples.append((zerogoodpastpart, metalabel, goodpastpart))

    # regular1 = (regularpastsg, regularpastpl, pastparticiple, pastpartwithe, wrongpastpart, wrongpastpart2, wrongpastpart2a, wrongenpastpart)
    # goodforms1 = (goodpastsg, goodpastpl, goodpastpart, goodpastpartwithe, goodpastpart, goodpastpart, goodpastpart, goodpastpart)
    # metanames1 = (overgen, overgen, overgen, overgen, wrongovergen, wrongovergen, wrongovergen, wrongovergen,)
    #
    # regular2 = (epastparticiple, zeropastparticiple, epastpartwithe, zeropastpartwithe, ewrongpastpart,
    #             zerowrongpastpart, ewrongenpastpart, zerowrongenpastpart, egoodpastpart, zerogoodpastpart)
    # goodforms2 = (goodpastpart, goodpastpart, goodpastpartwithe, goodpastpartwithe, goodpastpart,
    #               goodpastpart, goodpastpart, goodpastpart, goodpastpart, goodpastpart)
    #
    # regular = regular1 + regular2
    # goodforms = goodforms1 + goodforms2
    # return [regular, goodforms]
    return triples

# initialisation


# read the correctionfile
# eigenlijk nog de inflectiecode erbij@@@
correction = {}
correctionfile = open(os.path.join(SD_DIR, correctionfilename), 'r', encoding='utf8')
myreader = csv.reader(correctionfile, delimiter=tab)
for row in myreader:
    wrong = row[0]
    good = row[1]
    meta = row[2]
    correction[wrong] = good, meta
