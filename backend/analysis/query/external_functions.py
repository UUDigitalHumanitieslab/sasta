import re
from .compounds import getcompounds
from .Sziplus import sziplus6, vr5plus
from .xenx import xenx
from .imperatives import wx, wxy, wxyz, wxyz5, wondx, wond4, wond5plus
from .TARSPscreening import tarsp_screening
from .TARSPpostfunctions import vutotaal, gofase, gtotaal, pf2, pf3, pf4, pf5, pf6, pf7, pf
from .queryfunctions import xneg_x, xneg_neg
from dedup import mlux, samplesize, neologisme, onvolledig, correct
# from STAPpostfunctions import BB_totaal, GLVU, GL5LVU
from .ASTApostfunctions import wordcountperutt, countwordsandcutoff, KMcount, finietheidsindex, getlemmas
# from astaforms import astaform
# from tarspform import mktarspform

normalfunctionpattern = r'<function\s+(\w+)\b'
builtinfunctionpattern = r'<built-in function\s+(\w+)\b'


def getfname(f):
    fstr = str(f)
    m = re.match(normalfunctionpattern, fstr)
    if m is not None:
        result = m.group(1)
    else:
        m = re.match(builtinfunctionpattern, fstr)
        if m is not None:
            result = m.group(1)
        else:
            result = ''
    return result


# Initialisation
# thetarspfunctions = [getcompounds, sziplus6, xenx, vr5plus, wx, wxy, wxyz, wxyz5, wondx, wond4, wond5plus,
#                      tarsp_screening, vutotaal, gofase, gtotaal, pf2, pf3, pf4, pf5, pf6, pf7, pf, xneg_x, xneg_neg, mktarspform]
thetarspfunctions = [getcompounds, sziplus6, xenx, vr5plus, wx, wxy, wxyz, wxyz5, wondx, wond4, wond5plus,
                     tarsp_screening, vutotaal, gofase, gtotaal, pf2, pf3, pf4, pf5, pf6, pf7, pf, xneg_x, xneg_neg]

# thestapfunctions = [BB_totaal, GLVU, GL5LVU]


# theastafunctions = [samplesize, mlux, neologisme, onvolledig, correct,
#                     wordcountperutt, countwordsandcutoff, astaform, KMcount, finietheidsindex, getlemmas]
theastafunctions = [samplesize, mlux, neologisme, onvolledig, correct,
                    wordcountperutt, countwordsandcutoff, KMcount, finietheidsindex, getlemmas]

# thefunctions = thetarspfunctions + thestapfunctions + theastafunctions
thefunctions = theastafunctions + thetarspfunctions

str2functionmap = {}

for f in thefunctions:
    fname = getfname(f)
    str2functionmap[fname] = f
