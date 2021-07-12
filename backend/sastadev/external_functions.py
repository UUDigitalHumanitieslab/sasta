import re

from sastadev.asta_queries import asta_bijzin, asta_noun
from sastadev.ASTApostfunctions import (KMcount, countwordsandcutoff,
                                        finietheidsindex, getlemmas,
                                        wordcountperutt)
from sastadev.compounds import getcompounds
from sastadev.dedup import correct, mlux, neologisme, onvolledig, samplesize
from sastadev.imperatives import wond4, wond5plus, wondx, wx, wxy, wxyz, wxyz5
from sastadev.queryfunctions import VzN, xneg_neg, xneg_x
from sastadev.STAPpostfunctions import GL5LVU, GLVU, BB_totaal
from sastadev.Sziplus import sziplus6, vr5plus
from sastadev.astaforms import astaform
from sastadev.tarspform import mktarspform
from sastadev.TARSPpostfunctions import (gofase, gtotaal, pf, pf2, pf3, pf4,
                                         pf5, pf6, pf7, vutotaal)
from sastadev.TARSPscreening import tarsp_screening
from sastadev.xenx import xenx

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
thetarspfunctions = [getcompounds, xenx, sziplus6, vr5plus, wx,
                     wxy, wxyz, wxyz5, wondx, wond4,
                     wond5plus, tarsp_screening, vutotaal, gofase, gtotaal,
                     pf2, pf3, pf4, pf5, pf6,
                     pf7, pf, xneg_x, xneg_neg, VzN]
thestapfunctions = [BB_totaal, GLVU, GL5LVU]
theastafunctions = [samplesize, mlux, neologisme, onvolledig, correct,
                    wordcountperutt, countwordsandcutoff, KMcount, finietheidsindex, getlemmas,
                    asta_noun, asta_bijzin]

thefunctions = thetarspfunctions + thestapfunctions + theastafunctions


str2functionmap = {}

for f in thefunctions:
    fname = getfname(f)
    str2functionmap[fname] = f

form_map = {
    'TARSP': mktarspform,
    'ASTA': astaform
}
