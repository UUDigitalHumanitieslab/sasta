import re

interpunctionpattern = r'[\[]]!"#$%&\'\(\)\*\+,\-\./^_`{|}~@=\:;<>?]'
ch_finalinterpunctionpattern = r'[\[\]!"#$%&\'\(\*\+,\-\./^_`{|}~@=\:;<>?]'  # ) left out
ch_initialinterpunctionpattern = r'[\[\]!"#$%\'\)\*\+,\-\./^_`{|}~@=\:;<>?]'  # ( and & left out

initpattern = r'^(' + ch_initialinterpunctionpattern + r')(.*)$'
initre = re.compile(initpattern)
finalpattern = r'^(.*)(' + ch_finalinterpunctionpattern + r')$'
finalre = re.compile(finalpattern)


def tokenise(str):
    # split by spaces
    toklist1 = str.split()
    # remove final interpunction
    toklist2 = []
    for tok in toklist1:
        curtokpart = tok
        finallist = []
        while True:
            m = finalre.match(curtokpart)
            if m is None:
                if curtokpart != '':
                    toklist2.append(curtokpart)
                toklist2 = toklist2 + finallist
                break
            else:
                finallist = [m.group(2)] + finallist
                curtokpart = m.group(1)

    # remove initital punctuation
    toklist3 = []
    for tok in toklist2:
        curtokpart = tok
        while True:
            m = initre.match(curtokpart)
            if m is None:
                if curtokpart != '':
                    toklist3.append(curtokpart)
                break
            else:
                toklist3.append(m.group(1))
                curtokpart = m.group(2)
    return toklist3
