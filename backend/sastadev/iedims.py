import re

from sastadev import lexicon

comma = ','
semicolon = ';'
bigfilesep = semicolon
slash = '/'
epsilon = ''
vertbar = '|'


def bracket(str):
    result = r'(' + str + r')'
    return result


def drop(pattern, chars):
    lpattern = [c for c in pattern]
    newlpattern = [c for c in lpattern if c not in chars]
    newpattern = epsilon.join(newlpattern)
    return newpattern


def regexor(stringlist):
    result = vertbar.join(stringlist)
    return result


def makecic1j():
    parts = []
    for c in c1:
        if c not in '[]':
            newpart1 = drop(call, c1)
            newpart = '[' + newpart1 + ']' + c
            parts.append(newpart)
    pattern = regexor(parts)
    return pattern


begin = r'^(.*)'

vowel = r'[aeiouy]'
bvowel = bracket(vowel)
call = r'[bcdfghjklmnpqrstvwxz]'
bcall = bracket(call)
wb = '^'
callorwb = call + '|' + wb
bcallorwb = bracket(callorwb)
doublevowel = r'aa|ee|oo|uu'
diphthong = 'au|ei|eu|ie|ij|oe|ou|ui'
c1 = r'[pfksg]'
bc1 = bracket(c1)
ie = r'(ie)'
s = '(s?)'
end = r'$'
v4 = r'\4'
v3 = r'\3'
v2 = r'\2'
twovowels = doublevowel + '|' + diphthong
btwovowels = bracket(twovowels)
bdiphthong = bracket(diphthong)
cic1j = makecic1j()
bcic1j = bracket(cic1j)

# vvssie meissie -> meisje; Keessie -> keessie; feessie -> feestje; generalized to also wijffie -> wijfje, lieffie -> liefje, boekkie -> boekkie;
vvssiepattern = begin + btwovowels + bc1 + v3 + r'ie' + s + end
vvssiere = re.compile(vvssiepattern)
vvssiereplace = r'\1\2\3je\4'
vvssiereplacet = r'\1\2\3tje\4'

# the same as vvssie but now with a single consonant, so vvsie: koopie, weekie, feesie, beesie
vvsiepattern = begin + btwovowels + bc1 + r'ie' + s + end
vvsiere = re.compile(vvsiepattern)
vvsiereplace = r'\1\2\3je\4'
vvsiereplacet = r'\1\2\3tje\4'


# CVCiCiie -> VCije  bakkie -> bakje ukkie -> ukje
cvcicipattern = begin + bcallorwb + bvowel + bc1 + v4 + ie + s + end
cvcicire = re.compile(cvcicipattern)
cvcicireplace = r'\1\2\3\4je\6'
cvcicireplacet = r'\1\2\3\4tje\6'

# DCie -> V2Cje  buikie > buikje wijfie -> wijfje buisie _-> buisje poepie -> poepje
dciepattern = begin + bdiphthong + bc1 + r'ie' + s + end
dciere = re.compile(dciepattern)
dciereplace = r'\1\2\3je\4'

# CiC1jie -> C1C2je bankie -> bankje binkie -> binkje bloempie -> bloempje truckie -> truckje mamsie -> mamsje mensie -> mensje
cic1jiepattern = begin + bcic1j + r'ie' + s + end
cic1jiere = re.compile(cic1jiepattern)
cic1jiereplace = r'\1\2je\3'


# test
# testlist = [('bankie', 'bankje'), ('bloempie', 'bloempje'), ('truckie', 'truckje'), ('mensie', 'mensje')]
# localtest(cic1jiere, [cic1jre], testlist)


chiepattern = begin + r'chie' + s + end
chiere = re.compile(chiepattern)
chiereplace = r'\1chje\2'
chiereplacet = r'\1chtje\2'

# test
# testlist = [('hachie', 'hachje'), ('vrachie', 'vrachtje'),  ('kuchie', 'kuchje')]
# localtest(chiere, [chiereplace, chiereplacet], testlist)


# Cvssie messie -> mesje; schoffie -> schoftje; etc. niet voor effie -> efje; actually not needed coverd by cvcicipattern
cvssiepattern = begin + bcall + bvowel + bc1 + v4 + r'ie' + s + end
cvssiere = re.compile(cvssiepattern)
cvssiereplace = r'\1\2\3\4je\5'
cvssiereplacet = r'\1\2\3\4tje\5'

# test
# testlist = [('messie', 'mesje'), ('zakkie', 'zakje'), ('schriffie', 'schriftje')]
# localtest(cvssiere, [cvssiereplace, cvssiereplacet], testlist)


vciepattern = begin + bvowel + bcall + r'ie' + s + end
vciere = re.compile(vciepattern)
vciereplace = r'\1\2\2\3je\4'
# test
# testlist = [('slapie', 'slaapje'), ('rapie', 'raapje'), ('takie', 'taakje'), ('stafie', 'staafje'), ('magie', 'maagje'),
#            ('vasie', 'vaasje')]
# localtest(vciere, [vciereplace], testlist)

# getbase regexes:
ngetjepattern = begin + r'ngetje' + s + end     # tekeningetje
ngetjere = re.compile(ngetjepattern)
ngetjereplace = r'\1ng\2'

# testlist = [('tekeningetje','tekening'), ('tekeningetjes', 'tekening]
# localtest(ngetjere, [ngetjereplace], testlist)

cicietjepattern = begin + bcall + v2 + r'etje' + s + end  # balletje
cicietjere = re.compile(cicietjepattern)
cicietjereplace = r'\1\2'

# testlist = [('balletje','bal'), ('balletjes','bal')]
# localtest(cicietjere, [cicietjereplace], testlist)

cmpjepattern = begin + bcall + r'mpje' + s + end  # darmpje, armpje
cmpjere = re.compile(cmpjepattern)
cmpjereplace = r'\1\2m'

# testlist = [('armpje', 'arm'), ('armpjes', 'arm'), ('darmpje', 'darm'), ('darmpjes', 'darm')]
# localtest(cmpjere, [cmpjereplace], testlist)

vmpjepattern = begin + bcall + bracket(regexor([btwovowels, 'e'])) + r'mpje' + s + end  # bloempje, bezempje
vmpjere = re.compile(vmpjepattern)
vmpjereplace = r'\1\2\3m'

# testlist = [('bloempje','bloem'), ('bezempje', 'bezem'), ('bloempjes', 'bloem'), ('bezempjes', 'bezem')]
# localtest(vmpjere, [vmpjereplace], testlist)


nkjepattern = begin + r'nkje' + s + end   # koninkje
nkjere = re.compile(nkjepattern)
nkjereplace = r'\1ng'

# testlist = [('koninkje','koning'), ('koninkjes','koning')]
# localtest(nkjere, [nkjereplace], testlist)


vivitjepattern = begin + bvowel + v2 + r'tje' + s + end  # laatje
vivitjere = re.compile(vivitjepattern)
vivitjereplace = r'\1\2'

# testlist = [('laatje','la'), ('laatjes','la')]
# localtest(vivitjere, [vivitjereplace], testlist)


vivjtjepattern = begin + bdiphthong + r'tje' + s + end   # lelietje, leitje
vivjtjere = re.compile(vivjtjepattern)
vivjtjereplace = r'\1\2'

# testlist = [('lelietje','lelie'), ('leitje', 'lei'), ('lelietjes','lelie'), ('leitjes', 'lei')]
# localtest(vivjtjere, [vivjtjereplace], testlist)


jepattern = begin + r'je' + s + end  # huisje, bakje
jere = re.compile(jepattern)
jereplace = r'\1'

# testlist = [('huisje','huis'), ('bakje', 'bak'), ('huisjes','huis'), ('bakjes', 'bak')]
# localtest(jere, [jereplace], testlist)


voiceless = 'pst'
voiced = 'bzd'


def voicing(str):
    theindex = voiceless.find(str[0])
    if theindex >= 0:
        result = voiced[theindex]
    else:
        result = str
    return result


def getbaseinlexicon(dim):
    result = None
    candidates = getbase(dim)
    for candidate in candidates:
        if lexicon.informlexicon(candidate):
            result = candidate
            break
    return result


def getbase(dim):
    results = []
    if ngetjere.match(dim):
        newresult = ngetjere.sub(ngetjereplace, dim)
        results.append(newresult)
    if cicietjere.match(dim):
        newresult = cicietjere.sub(cicietjereplace, dim)
        results.append(newresult)
    if cmpjere.match(dim):
        newresult = cmpjere.sub(cmpjereplace, dim)
        results.append(newresult)
    if vmpjere.match(dim):
        newresult = vmpjere.sub(vmpjereplace, dim)
        results.append(newresult)
    if nkjere.match(dim):
        newresult = nkjere.sub(nkjereplace, dim)
        results.append(newresult)
    if vivitjere.match(dim):
        newresult = vivitjere.sub(vivitjereplace, dim)
        results.append(newresult)
    if vivjtjere.match(dim):
        newresult = vivjtjere.sub(vivjtjereplace, dim)
        results.append(newresult)
    if jere.match(dim):
        newresult = jere.sub(jereplace, dim)
        results.append(newresult)
    return results


def getjeforms(ieform):
    results1 = getjeformsnolex(ieform)
    resultset = set(results1)
    results = []
    for result in resultset:
        if lexicon.informlexicon(result):
            # result = '[ @add_lex {} {} ]'.format(ieform, result)
            results.append(result)
    return results


def getjeformsnolex(ieform):
    results = []
    if cvcicire.match(ieform):
        m = cvcicire.match(ieform)
        result = cvcicire.sub(cvcicireplace, ieform)
        results.append(result)
        result = cvcicire.sub(cvcicireplacet, ieform)
        results.append(result)
        bdg = voicing(m.group(4))
        result = cvcicire.sub(r'\1\2\3' + bdg + r'je\6', ieform)
        results.append(result)
    elif dciere.match(ieform):
        m = dciere.match(ieform)
        result = dciere.sub(dciereplace, ieform)
        results.append(result)
        bdg = voicing(m.group(3))
        result = cvcicire.sub(r'\1\2' + bdg + r'je\4', ieform)
        results.append(result)
    elif vvssiere.match(ieform):
        # m = vvssiere.match(ieform)
        result = vvssiere.sub(vvssiereplace, ieform)
        results.append(result)
        result = vvssiere.sub(vvssiereplacet, ieform)
        results.append(result)
    elif vvsiere.match(ieform):
        # m = vvsiere.match(ieform)
        result = vvsiere.sub(vvsiereplace, ieform)
        results.append(result)
        result = vvsiere.sub(vvsiereplacet, ieform)
        results.append(result)
    elif vciere.match(ieform):  # must crucially occur after the previous two (otherwise beesie -> beeestje)
        # m = vciere.match(ieform)
        result = vciere.sub(vciereplace, ieform)
        results.append(result)
    elif chiere.match(ieform):
        # m = chiere.match(ieform)
        result = chiere.sub(chiereplace, ieform)
        results.append(result)
        result = chiere.sub(chiereplacet, ieform)
        results.append(result)
    elif cic1jiere.match(ieform):
        # m = cic1jiere.match(ieform)
        result = cic1jiere.sub(cic1jiereplace, ieform)
        results.append(result)
    else:
        results = []
    return results
