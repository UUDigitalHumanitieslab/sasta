import logging
from typing import Counter, Dict, List, Match, Optional, Tuple, Union

from lxml import etree as ET

logger = logging.getLogger('sasta')


class UtteranceWord:
    def __init__(self, word, begin, end,
                 hits, zc_embedding=None):
        self.word: str = word
        self.begin: int = int(begin)
        self.end: int = int(end)
        self.hits: List[Dict] = hits
        self.zc_embedding: Optional[int] = zc_embedding

    def __str__(self):
        return f'{self.word}({self.begin}:{self.end})({len(self.hits)})'

    def __repr__(self):
        return self.__str__()


QueryTuple = Tuple[str, str]
SynTree = Union[ET._Element, str]
# TODO: Match type
SastaMatch = Tuple[Match, SynTree]
SastaMatchList = List[SastaMatch]
SastaMatches = Dict[QueryTuple, SastaMatchList]
SastaResults = Dict[str, Counter[str]]
SastaAnnotations = Dict[str, List[UtteranceWord]]


class AllResults:
    def __init__(self,
                 filename,
                 uttcount,
                 coreresults=None,
                 postresults=None,
                 allmatches=None,
                 annotations=None,
                 analysedtrees=None):
        self.filename: str = filename
        self.uttcount: int = uttcount
        self.coreresults: SastaResults = coreresults or {}
        self.postresults: SastaResults = postresults or {}
        self.allmatches: SastaMatches = allmatches or tuple()
        self.annotations: SastaAnnotations = annotations or {}
        self.analysedtrees: List[SynTree] = analysedtrees or []

    def __repr__(self):
        return f'name: {self.filename}, core: {len(self.coreresults)}, post: {len(self.postresults)}, matches: {len(self.allmatches)}'  # noqa: E501


def scores2counts(scores):
    '''
    input is a dictionary of Counter()s
    output is a dictionary of ints
    '''
    counts = {}
    for el in scores:
        countval = len(scores[el])
        counts[el] = countval
    return counts
