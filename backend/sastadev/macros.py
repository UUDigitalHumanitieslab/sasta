import re
from . import SDLOGGER, SD_DIR
import os.path as op

idpat = r'([A-z_][A-z0-9_]*)'
eqpat = r'='
exprpat = r'"""(.*?)"""'
whitespaces = r'\s+'

macrocallpat = r'(%.+?%)'
macrocallre = re.compile(macrocallpat)

macropat = idpat + whitespaces + eqpat + whitespaces + exprpat

macrore = re.compile(macropat, re.S)


def macrostrs2dict(teststrings):
    macrodict = {}
    for tstr in teststrings:
        macromatches = macrore.finditer(tstr)
        for macromatch in macromatches:
            macroname = macromatch.group(1)
            macroexpr = macromatch.group(2)
            macrodict[macroname] = macroexpr

    return macrodict


def readmacros(macrofile, macrodict):
    macrotext = macrofile.read()
    macromatches = macrore.finditer(macrotext)
    for macromatch in macromatches:
        macroname = macromatch.group(1)
        macroexpr = macromatch.group(2)
        if macroname in macrodict:
            SDLOGGER.warning('Duplicate macro {} encountered. Ignored'.format(macroname))
        else:
            macrodict[macroname] = macroexpr
    return macrodict


def expandmacros(expr):
    result = expandmacrosdict(expr, macrodict)
    return result


def expandmacrosdict(expr, macrodict):
    newexpr = expr
    thematch = macrocallre.search(newexpr)
    while thematch:
        macrocall = thematch.group(1)
        macroname = macrocall[1:-1]
        if macroname in macrodict:
            thismacrocallre = re.compile(macrocall)
            newexpr = thismacrocallre.sub(macrodict[macroname], newexpr)
            thematch = macrocallre.search(newexpr)
        else:
            SDLOGGER.error('Unknown macro call encountered: {}.'.format(macroname))
            break
    return newexpr


macrodir = op.join(SD_DIR, 'macros')
macrofilenames = [op.join(macrodir, 'sastamacros1.txt'), op.join(macrodir, 'sastamacros2.txt')]

macrodict = {}
for macrofilename in macrofilenames:
    macrofile = open(macrofilename, 'r', encoding='utf8')
    macrodict = readmacros(macrofile, macrodict)
