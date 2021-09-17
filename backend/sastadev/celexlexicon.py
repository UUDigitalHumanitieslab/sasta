import csv
import os
import re
import sys
from collections import defaultdict

from sastadev import SD_DIR, treebankfunctions

backslash = '\\'
celexsep = backslash

pospattern = r'^.*\[(?P<pos>.)\]$'
posre = re.compile(pospattern)

# dml columns
IdNum, Head, Inl, MorphStatus, MorphCnt, DerComp, Comp, Def, Imm, \
    ImmSubCat, ImmAllo, ImmSubst, StrucLab, StrucAllo, StrucSubst, Sepa = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

no_t_verbs = {'mogen', 'kunnen', 'zullen', 'willen'}

logfile = sys.stderr

# initialisation
# read the celex lexicon
inputfolder = os.path.join(SD_DIR, 'celexlexicon', 'dutch')

dmwfilename = 'DMWCDOK.txt'
dmwfullname = os.path.join(inputfolder, dmwfilename)
dmwdict = {}
dmwlemmakeyinflindex = defaultdict(list)
dmwkeydict = {}

# dmw columns: recid, form, lemmakey, pos, infl


with open(dmwfullname, mode='r') as infile:
    myreader = csv.reader(infile, delimiter=celexsep)
    for row in myreader:
        thekey = row[0]
        dmwkeydict[thekey] = row
        theform = row[1]
        if theform in dmwdict:
            dmwdict[theform].append(thekey)
        else:
            dmwdict[theform] = [thekey]
        lemmainflkey = (row[3], row[4])
        dmwlemmakeyinflindex[lemmainflkey].append(row[0])

dmlfilename = 'DMLCD.txt'
dmlfullname = os.path.join(inputfolder, dmlfilename)
dmldict = {}

with open(dmlfullname, mode='r') as infile:
    myreader = csv.reader(infile, delimiter=celexsep)
    for row in myreader:
        thekey = row[IdNum]
        if thekey in dmldict:
            print('Warning: Duplicate key in dmlcd: {}'.format(thekey), file=logfile)
        dmldict[thekey] = row


# The dsl.cd file contains the following fields:
dslIdNum, dslHead, dslInl, dslClassNum, dslGendNum, dslDeHetNum, dslPropNum, \
    dslAuxNum, dslSubClassVNum, dslSubCatNum, dslAdvNum, dslCardOrdNum, dslSubClassPNum = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12

posnum2pos = {'0': 'None', '1': 'n', '2': 'adj', '3': 'tw', '4': 'ww', '5': 'lid', '6': 'vnw', '7': 'bw', '8': 'vz', '9': 'vw', '10': 'tsw'}
pos2posnum = {posnum2pos[key]: key for key in posnum2pos}


dslfilename = 'DSLCD.txt'
dslfullname = os.path.join(inputfolder, dslfilename)
dsldict = {}
dsllemmaposindex = defaultdict(list)


with open(dslfullname, mode='r') as infile:
    myreader = csv.reader(infile, delimiter=celexsep)
    for row in myreader:
        thekey = row[dslIdNum]
        if thekey in dsldict:
            print('Warning: Duplicate key in dslcd: {}'.format(thekey), file=logfile)
        dsldict[thekey] = row
        lemmaposkey = (row[dslHead], row[dslClassNum])
        dsllemmaposindex[lemmaposkey].append(thekey)


def dcoiphi2celexpv(thesubj, thepv, inversion):
    '''
    :param thesubj: subject node
    :param thepv: finite verb node
    :param inversion: True or False
    :return:
    '''
    (rawperson, number, _) = treebankfunctions.getphi(thesubj)
    lemma = treebankfunctions.getlemma(thesubj)
    if lemma in ['het']:
        person = '3'
        number = 'ev'
    else:
        person = '3' if rawperson == '' else rawperson
    tense = treebankfunctions.getattval(thepv, 'pvtijd')
    pvnumber = treebankfunctions.getattval(thepv, 'pvagr')
    celexperson = person[0] if person != '' and ((number in ['ev', 'getal'] and tense == 'tgw') or (tense == '')) else ''
    if number != 'getal' and number != '':
        celexnumber = number[0]
    elif lemma in ['je']:
        celexnumber = 'e'
    elif celexperson in ['1', '2', '3']:
        celexnumber = 'e'
    elif pvnumber == 'met-t':
        celexnumber = 'e'
    elif pvnumber == '':
        celexnumber = 'm'  # assuming that we are dealing with an infinitive
    else:
        celexnumber = pvnumber[0]
    celextense = tense[0] if tense != '' else 't'  # in case a verb is analysed as inf instead of as  pv
    celexinversion = 'I' if inversion else ''
    result = celextense + celexnumber + celexperson + celexinversion
    return result


celex2dcoimap = {'te1': {'pvtijd': 'tgw', 'pvagr': 'ev', 'wvorm': 'pv'},
                 'te2': {'pvtijd': 'tgw', 'pvagr': 'ev', 'wvorm': 'pv'},
                 'te2t': {'pvtijd': 'tgw', 'pvagr': 'met-t', 'wvorm': 'pv'},
                 'te3': {'pvtijd': 'tgw', 'pvagr': 'ev', 'wvorm': 'pv'},
                 'te3t': {'pvtijd': 'tgw', 'pvagr': 'met-t', 'wvorm': 'pv'},
                 'te2I': {'pvtijd': 'tgw', 'pvagr': 'ev', 'wvorm': 'pv'},
                 'tm': {'pvtijd': 'tgw', 'pvagr': 'mv', 'wvorm': 'pv'},
                 've': {'pvtijd': 'verl', 'pvagr': 'ev', 'wvorm': 'pv'},
                 'vm': {'pvtijd': 'verl', 'pvagr': 'mv', 'wvorm': 'pv'},
                 'i': {'wvorm': 'inf', 'positie': 'vrij', 'buiging': 'zonder'},
                 'pv': {'wvorm': 'vd', 'positie': 'vrij', 'buiging': 'zonder'},
                 'pt': {'wvorm': 'td', 'positie': 'vrij', 'buiging': 'zonder'},
                 'pvE': {'wvorm': 'vd', 'buiging': 'met-e', 'positie': 'prenom'},
                 'ptE': {'wvorm': 'td', 'buiging': 'met-e', 'positie': 'prenom'}
                 }


def celexpv2dcoi(word, infl, lemma):
    results = []
    if infl not in celex2dcoimap:
        results = []
    elif infl in {'te2', 'te3'}:
        if lemma[-3] == 't':
            results = celex2dcoimap[infl]
        elif lemma in no_t_verbs:
            results = celex2dcoimap[infl]
        else:
            results = celex2dcoimap[infl + 't']
    else:
        results = celex2dcoimap[infl]
    return results


def incelexdmw(str):
    result = str in dmwdict
    return result


def incelexdmwpos(word, pos):
    result = incelexdmw(word)
    poslist = getposlist(word)
    result = result and pos in poslist
    return result


def getlemmas(word):
    lemmas = []
    lemmakeys = getlemmakeys(word)
    for lemmakey in lemmakeys:
        if lemmakey is not None:
            if lemmakey in dmldict:
                lemma = dmldict[lemmakey][1]
                lemmas.append(lemma)
            else:
                lemma = None
        else:
            lemma = None
    return lemmas


def getlemmakeys(word):
    lemmakeys = []
    if word in dmwdict:
        for key in dmwdict[word]:
            featurelist = dmwkeydict[key]
            lemmakey = featurelist[3]
            lemmakeys.append(lemmakey)
    else:
        lemmakeys = []
    return lemmakeys


def getdehet(lemmakey):
    if lemmakey in dsldict:
        dehet = dsldict[lemmakey][dslDeHetNum]
    else:
        dehet = None
    if dehet == '':
        dehet = 'n/a'
    return dehet


def oldgetpos(lemmakey):
    if lemmakey in dmldict:
        wordstructure = dmldict[lemmakey][StrucLab]
        m = posre.match(wordstructure)
        if m is not None:
            pos = m.group('pos')
        else:
            pos = 'None'
    else:
        pos = None
    return pos


def getpos(lemmakey):
    if lemmakey in dsldict:
        features = dsldict[lemmakey]
        posnum = features[dslClassNum]
        if posnum in posnum2pos:
            pos = posnum2pos[posnum]
        else:
            pos = 'None'
    return pos


def getposlist(word):
    poslist = []
    lemmakeys = getlemmakeys(word)
    for lemmakey in lemmakeys:
        pos = getpos(lemmakey)
        poslist.append(pos)
    return poslist


def getinfls(word):
    infls = []
    if word in dmwdict:
        for key in dmwdict[word]:
            featurelist = dmwkeydict[key]
            infl = featurelist[4]
            infls.append(infl)
    return infls


def getwordposinfo(word, pos):
    cands = getwordinfo(word)
    results = [(pt, dehet, infl, lemma) for (pt, dehet, infl, lemma) in cands if pt == pos]
    return results


def getwordinfo(word):
    pos_infl_lemmas = []
    if word in dmwdict:
        for key in dmwdict[word]:
            featurelist = dmwkeydict[key]
            infl = featurelist[4]
            lemmakey = featurelist[3]
            lemma = dmldict[lemmakey][1]
            pos = getpos(lemmakey)
            dehet = getdehet(lemmakey)
            pos_infl_lemmas.append((pos, dehet, infl, lemma))
    return pos_infl_lemmas


def getinflforms(lemma, numClass, infl):
    results = []
    lemmakeys = dsllemmaposindex[(lemma, numClass)]
    for lemmakey in lemmakeys:
        wordkeys = dmwlemmakeyinflindex[(lemmakey, infl)]
        for wordkey in wordkeys:
            results.append(dmwkeydict[wordkey][1])
    return results
