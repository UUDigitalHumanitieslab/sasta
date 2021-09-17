import csv
import os

from sastadev import SD_DIR

tab = '\t'
namepartlexicon = {}


def isa_namepart(word):
    return word in namepartlexicon


def isa_namepart_uc(word):
    if word is None or word == '':
        result = False
    else:
        uc = word[0].isupper()
        found = word in namepartlexicon
        result = uc and found
    return result


namepartfilename = os.path.join(SD_DIR, 'names', 'nameparts', 'namepartlexicon.csv')
with open(namepartfilename, 'r', encoding='utf8') as namepartfile:
    csvreader = csv.reader(namepartfile, delimiter=tab)
    for row in csvreader:
        namepart = row[0]
        frq = row[1]
        namepartlexicon[namepart] = frq
