import logging
import os
import re
from collections import Counter, defaultdict
from pprint import pprint
from typing import Any
from typing import Counter as CounterType
from typing import DefaultDict, Dict, List, Optional, Pattern, Tuple

import pandas as pd

from ..models import AssessmentMethod, AssessmentQuery

logger = logging.getLogger('sasta')


# Type annotations
TupleStrDict = Dict[Tuple[Optional[str], Optional[str]], str]
CounterDict = Dict[str, CounterType[str]]

# Global
ITEMSEPPATTERN = r'[,-; ]'
LABELSEP = ';'
UTTLEVEL = 'utt'
HEADER_VARIANTS = {
    'speaker': ['speaker', 'spreker', 'spk'],
    'utt_id': ['id', 'utt', 'uttid'],
    'level': ['level'],
    'phase': ['fases', 'stages'],
    'comments': ['comments', 'commentaar']
}
PREFIX = ""
ALTITEMSEP = IMPLIESSEP = ','


class SAFDocument:
    def __init__(self, name):
        self.name: str = name
        self.utterances: List[SAFUtterance] = []
        self.levels: List[str] = []

    @property
    def label_counts(self):
        return sum([u.label_counts for u in self.utterances], Counter())


class SAFUtterance:
    def __init__(self, utt_id):
        self.utt_id: int = utt_id
        self.words: List[SAFWord] = []

    @property
    def label_counts(self):
        return sum([w.label_counts for w in self.words], Counter())


class SAFWord:
    def __init__(self, idx, text):
        self.idx: int = idx
        self.text: str = text
        self.annotations: List[SAFAnnotation] = []

    @property
    def label_counts(self):
        return Counter({(a.level, a.label) for a in self.annotations})

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text


class SAFAnnotation:
    def __init__(self, level, label):
        self.level: str = level
        self.label: str = label

    def __repr__(self):
        return f'{self.level}, {self.label}'


def lowerc(item: Optional[str]) -> Optional[str]:
    return item if not item else item.lower()


def clean(cell: Any) -> Any:
    if isinstance(cell, str):
        result = cell
        result = result.lstrip()
        result = result.rstrip()
        result = result.lower()
        return result
    return cell


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


def enrich(labelstr: str, lcprefix: str) -> str:
    if not labelstr:
        return labelstr
    try:
        labels = labelstr.split(LABELSEP)
        newlabels = []
        for label in labels:
            # should already be cleaned
            cleanlabel = clean(label)
            if cleanlabel != "" and lcprefix != "":
                newlabels.append(lcprefix+":" + cleanlabel)
            else:
                newlabels.append(cleanlabel)
        result = LABELSEP.join(newlabels)
        return result
    except:
        logger.warning(f'non-str enrich: {labelstr} {type(labelstr)}')
        return labelstr


def getitem2levelmap(mapping: TupleStrDict):
    resultmap: DefaultDict[str, List[str]] = defaultdict(list)
    for (item, level) in mapping:
        if item and level:
            if item in resultmap:
                resultmap[item].append(level)
            else:
                resultmap[item] = [level]
    return resultmap


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


def mkpatterns(allcodes: List[str]) -> Tuple[Pattern, Pattern]:
    basepattern = r''
    sortedallcodes = sorted(allcodes, key=len, reverse=True)
    adaptedcodes = [codeadapt(c) for c in sortedallcodes]
    basepattern = r'' + '|'.join(adaptedcodes) + '|' + ITEMSEPPATTERN
    fullpattern = r'^(' + basepattern + r')*$'
    return(re.compile(basepattern), re.compile(fullpattern))


def read_headers(row):
    headers: Dict[str, str] = {}
    # for colctr in range(startcol, lastcol):
    #     headers[colctr] = sheet.cell_value(rowctr, colctr)
    #     if iswordcolumn(headers[colctr]):
    #         lastwordcol = colctr
    #         if isfirstwordcolumn(headers[colctr]):
    #             firstwordcol = colctr
    #     elif clean(headers[colctr]) in speakerheaders:
    #         spkcol = colctr
    #     elif clean(headers[colctr]) in uttidheaders:
    #         uttidcol = colctr
    #     elif clean(headers[colctr]) in levelheaders:
    #         levelcol = colctr
    #     elif clean(headers[colctr]) in stagesheaders:
    #         stagescol = colctr
    #     elif clean(headers[colctr]) in commentsheaders:
    #         commentscol = colctr
    for cell in row:
        pass


def standardize_header_name(header: str) -> str:
    '''lowercase and standardize header'''
    header = header.lower()
    for key, val in HEADER_VARIANTS.items():
        if header in val:
            return key
    return header


def parse_word(idx: int, colname: str,
               data_in: pd.DataFrame, patterns: Tuple[Pattern, Pattern]) -> Optional[SAFWord]:
    data = data_in.dropna()
    if data.empty:
        return None
    try:
        text = data[data.level == UTTLEVEL][colname].values[0]
    except (KeyError, IndexError):
        # empty word
        text = ''
    instance = SAFWord(idx, text)
    for level in [l for l in data.level.unique() if l != UTTLEVEL]:
        label = data[data.level == level][colname].values[0]

        enriched_label = enrich(label.lower(), PREFIX.lower())
        # labels = getlabels(enriched_label, patterns)

        # cleanlevelsandlabels = getcleanlevelsandlabels(
        #     thelabelstr, thelevel, PREFIX, patterns)

        instance.annotations.append(SAFAnnotation(
            clean(level), clean(enriched_label)))
    return instance


def parse_utterance(utt_id: int, data: pd.DataFrame, word_cols: List[str], patterns: Tuple[Pattern, Pattern]) -> SAFUtterance:
    instance = SAFUtterance(utt_id)
    words = [parse_word(i+1, wcol, data[['level', wcol]], patterns)
             for i, wcol in enumerate(word_cols)]
    instance.words = [w for w in words if w]
    return instance


def parse_annotations(data: pd.DataFrame) -> List[SAFUtterance]:
    pass


def pandas_read(infilename):
    data = pd.read_excel(infilename)
    data.rename(columns=standardize_header_name, inplace=True)
    # clean strings
    data.level = data.level.apply(clean)
    # replace np.nan by regular None
    data = data.where(data.notnull(), None)
    # all_levels = data.level.unique()
    data.dropna(how='all', axis=1, inplace=True)
    return data


def get_annotations(infilename, patterns: Tuple[Pattern, Pattern]):
    '''
    Reads the file with name filename in SASTA Annotation Format
    :param infilename:
    :param patterns
    :return: a dictionary  with as  key a tuple (level, item) and as value a Counter  with key uttid and value its count
    '''
    # thedata = defaultdict(list)
    # cdata = {}
    uttlevel = 'utt'
    prefix = ""
    doc = SAFDocument(os.path.basename(infilename))

    data = pandas_read(infilename)

    word_cols = [c for c in data.columns if c.startswith('word')]
    utterance_rows = data[['utt_id', 'level'] +
                          word_cols][data.level == uttlevel]
    non_utt_rows = data[word_cols+['level']][data.level != uttlevel]

    for idx in data.utt_id.unique():
        utt_data = data[data.utt_id == idx]
        doc.utterances.append(parse_utterance(
            idx, utt_data, word_cols, patterns))

    pprint(doc.label_counts)
    # total_counter = Counter()
    # data[word_cols] = data[word_cols].applymap(lambda x: enrich(
    #     x, prefix))
    # for wcol in word_cols:
    #     count = non_utt_rows.groupby('level')[wcol].value_counts()
    #     total_counter += count
    # pprint(total_counter)
    # return total_counter

    #         if sheet.cell_value(rowctr, uttidcol) != "":
    #             uttid = str(int(sheet.cell_value(rowctr, uttidcol)))
    #         thelevel = sheet.cell_value(rowctr, levelcol)
    #         thelevel = clean(thelevel)
    #         all_levels.add(thelevel)
    #         for colctr in range(firstwordcol, sheet.ncols):
    #             if thelevel != uttlevel and colctr != stagescol and colctr != commentscol:
    #                 thelabelstr = sheet.cell_value(rowctr, colctr)
    #                 thelevel = sheet.cell_value(rowctr, levelcol)
    #                 if lastwordcol+1 <= colctr < sheet.ncols:
    #                     # prefix = headers[colctr] aangepast om het simpeler te houden
    #                     prefix = ""
    #                 else:
    #                     prefix = ""
    #                 cleanlevelsandlabels = getcleanlevelsandlabels(
    #                     thelabelstr, thelevel, prefix, patterns)
    #                 for (cleanlevel, cleanlabel) in cleanlevelsandlabels:
    #                     thedata[(cleanlevel, cleanlabel)].append(uttid)
    # # wb.close() there is no way to close the workbook
    # for atuple in thedata:
    #     cdata[atuple] = Counter(thedata[atuple])
    # return cdata
    return None


def get_golddata(filename, mapping, altcodes, queries, includeimplies=False):
    item2levelmap = {}
    mappingitem2levelmap = getitem2levelmap(mapping)
    altcodesitem2levelmap = getitem2levelmap(altcodes)
    # Todo: None types??
    allmappingitems = [item for (item, _) in mapping if item]
    allaltcodesitems = [item for (item, _) in altcodes if item]
    allitems = allmappingitems + allaltcodesitems
    patterns = mkpatterns(allitems)
    basicdata = get_annotations(filename, patterns)
    # results = {}
    return allitems


def read_method(method: AssessmentMethod):
    queries: List[AssessmentQuery] = list(method.queries.all())
    item2idmap: TupleStrDict = {
        (lowerc(q.item), lowerc(q.level)): q.query_id for q in queries}
    altcodes: Dict[Any, Any] = {
        (lowerc(q.altitems), lowerc(q.level)): q.query_id for q in queries}
    postquerylist: List[str] = [q.query_id for q in queries if q.process == 1]
    return queries, item2idmap, altcodes, postquerylist


def read_annotations(method: AssessmentMethod, annotationfilename, includeimplies=False) -> None:
    '''
    :param includeimplies: a parameter to specify whether information in the implies column
    of the method must be taken into account (default False, keep it that way)
    '''
    (queries, item2idmap, altcodes, postquerylist) = read_method(method)
    annotationfilename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'test_sample.xlsx')
    richscores = get_golddata(
        annotationfilename, item2idmap, altcodes, queries, includeimplies)
    # results = richscores2scores(richscores)
    return None
