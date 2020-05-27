import re
from os.path import abspath
import logging

idpat = r'([A-z_][A-z0-9_]*)'
eqpat = r'='
exprpat = r'"""(.*?)"""'
whitespaces = r'\s+'

macrocallpat = r'(%.+?%)'
macrocallre = re.compile(macrocallpat)

macropat = idpat + whitespaces + eqpat + whitespaces + exprpat

macrore = re.compile(macropat, re.S)

MACROFILENAMES = ['analysis/macros/sastamacros1.txt',
                  'analysis/macros/sastamacros2.txt']


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
            logging.warning(
                'Duplicate macro {} encountered. Ignored'.format(macroname))
        else:
            macrodict[macroname] = macroexpr
    return macrodict


def expandmacros(expr, macrodict):
    result = expandmacrosdict(expr, macrodict)
    return result


def expandmacrosdict(expr, macrodict):
    newexpr = expr
    thematch = macrocallre.search(newexpr)
    while thematch:
        macrocall = thematch.group(1)
        macroname = macrocall[1:-1]
        if macroname in macrodict:
            newexpr = macrocallre.sub(macrodict[macroname], newexpr)
            thematch = macrocallre.search(newexpr)
        else:
            logging.error(
                'Unknown macro call encountered: {}.'.format(macroname))
            break
    return newexpr


def get_macros_dict(macrofilenames=MACROFILENAMES):
    macrodict = {}
    for macrofilename in macrofilenames:
        macrofile = open(abspath(macrofilename), 'r', encoding='utf8')
        macrodict = readmacros(macrofile, macrodict)
    return macrodict
