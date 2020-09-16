import logging
import re
from typing import List, Pattern, Tuple

from .config import HEADER_VARIANTS, ITEMSEPPATTERN, LABELSEP, TupleStrDict

logger = logging.getLogger('sasta')


def standardize_header_name(header: str) -> str:
    '''lowercase and standardize header'''
    header = header.lower()
    for key, val in HEADER_VARIANTS.items():
        if header in val:
            return key
    return header


def clean_cell(cell):
    if isinstance(cell, str):
        result = cell
        result = result.lstrip()
        result = result.rstrip()
        result = result.lower()
        return result
    return cell


def mkpatterns(allcodes: List[str]) -> Tuple[Pattern, Pattern]:
    basepattern = r''
    sortedallcodes = sorted(allcodes, key=len, reverse=True)
    adaptedcodes = [codeadapt(c) for c in sortedallcodes]
    basepattern = r'' + '|'.join(adaptedcodes) + '|' + ITEMSEPPATTERN
    fullpattern = r'^(' + basepattern + r')*$'

    return(re.compile(basepattern), re.compile(fullpattern))


def codeadapt(code: str) -> str:
    result = code
    result = re.sub(r'\.', r'\\.', result)
    result = re.sub(r'\(', r'\\(', result)
    result = re.sub(r'\)', r'\\)', result)
    result = re.sub(r'\?', r'\\?', result)
    result = re.sub(r'\*', r'\\*', result)
    result = re.sub(r'\+', r'\\+', result)
    result = re.sub(r' ', r'\\s+', result)

    return result


def enrich(labelstr: str, lcprefix: str) -> str:
    if not labelstr:
        return labelstr
    try:
        labels = labelstr.split(LABELSEP)
        newlabels = []
        for label in labels:
            if label != "" and lcprefix != "":
                newlabels.append(lcprefix+":" + label)
            else:
                newlabels.append(label)
        result = LABELSEP.join(newlabels)
        return result
    except TypeError:
        logger.warning('non-str enrich: %s %s', labelstr, type(labelstr))
        return labelstr


def getlabels(labelstr, patterns):
    results = []
    (pattern, fullpattern) = patterns
    if fullpattern.match(labelstr):
        matches = pattern.finditer(labelstr)
        results = [m.group(0) for m in matches if m.group(0) not in ' ;,-/']
    else:
        results = []
        matches = pattern.finditer(labelstr)
        logstr = str([m.group(0) for m in matches if m.group(0) not in ' ;,-'])
        logger.warning('Cannot interpret %s; found items: %s',
                       labelstr, logstr)
    return results


def item2queryid(item: str, level: str,
                 mapping: TupleStrDict):
    if (item, level) in mapping:
        return mapping[(item, level)]
    return None
