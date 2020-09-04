import csv
import os
import sys
import re

backslash = '\\'
celexsep = backslash

pospattern = r'^.*\[(?P<pos>.)\]$'
posre = re.compile(pospattern)

# dml columns
IdNum, Head, Inl, MorphStatus, MorphCnt, DerComp, Comp, Def, Imm, \
    ImmSubCat, ImmAllo, ImmSubst, StrucLab, StrucAllo, StrucSubst, Sepa = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

logfile = sys.stderr

# initialisation
# read the celex lexicon
programfolder = os.path.dirname(os.path.abspath(__file__))
inputfolder = os.path.join(programfolder, 'celexlexicon', 'dutch')

dmwfilename = 'dmwcdok.txt'

dmwfullname = os.path.join(inputfolder, dmwfilename)
dmwdict = {}

with open(dmwfullname, mode='r') as infile:
    myreader = csv.reader(infile, delimiter=celexsep)
    for row in myreader:
        thekey = row[1]
        if thekey in dmwdict:
            dmwdict[thekey].append(row)
        else:
            dmwdict[thekey] = [row]

dmlfilename = 'dmlcd.txt'
dmlfullname = os.path.join(inputfolder, dmlfilename)
dmldict = {}

with open(dmlfullname, mode='r') as infile:
    myreader = csv.reader(infile, delimiter=celexsep)
    for row in myreader:
        thekey = row[IdNum]
        if thekey in dmldict:
            print('Warning: Duplicate key in dmlcd: {}'.format(
                thekey), file=logfile)
        dmldict[thekey] = row


# The dsl.cd file contains the following fields:
#
dslIdNum, dslHead, dslInl, dslClassNum, dslGendNum, dslDeHetNum, dslPropNum, \
    dslAuxNum, dslSubClassVNum, dslSubCatNum, dslAdvNum, dslCardOrdNum, dslSubClassPNum = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12


dslfilename = 'dslcd.txt'
dslfullname = os.path.join(inputfolder, dslfilename)
dsldict = {}

with open(dslfullname, mode='r') as infile:
    myreader = csv.reader(infile, delimiter=celexsep)
    for row in myreader:
        thekey = row[dslIdNum]
        if thekey in dsldict:
            print('Warning: Duplicate key in dslcd: {}'.format(
                thekey), file=logfile)
        dsldict[thekey] = row


def incelexdmw(str):
    result = str in dmwdict
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
        for featurelist in dmwdict[word]:
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


def getpos(lemmakey):
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
        for featurelist in dmwdict[word]:
            infl = featurelist[4]
            infls.append(infl)
        else:
            infl = None
    return infls


def getwordinfo(word):
    pos_infl_lemmas = []
    if word in dmwdict:
        for featurelist in dmwdict[word]:
            infl = featurelist[4]
            lemmakey = featurelist[3]
            lemma = dmldict[lemmakey][1]
            pos = getpos(lemmakey)
            dehet = getdehet(lemmakey)
            pos_infl_lemmas.append((pos, dehet, infl, lemma))
    return pos_infl_lemmas


def test():
    testwords = ['liepen', 'gevalt', 'gevallen', 'mouwen', 'stukjes',
                 'vaak', 'mooi', 'gouden', 'mooie', 'mooiere', 'pop', 'popje']
    for w in testwords:
        #poslist = getposlist(w)
        #lemmas = getlemmas(w)
        #infls = getinfls(w)
        #print(w, lemmas,  poslist, infls)
        graminfos = getwordinfo(w)
        for (pos, dehet, infl, lemma) in graminfos:
            print(w, lemma, pos, dehet, infl)


if __name__ == '__main__':
    test()
