import logging
from typing import Counter, Dict, List, Match, Optional, Tuple, Union

from lxml import etree as ET

logger = logging.getLogger('sasta')


class UtteranceWord:
    def __init__(self, word, begin, end,
                 hits, idx=None, zc_embedding=None, comments=None):
        self.word: str = word
        self.begin: int = int(begin)
        self.end: int = int(end)
        self.hits: List[Dict] = hits
        self.index: Optional[int] = idx  # 0 for unaligned, then 1...n for words
        self.zc_embedding: Optional[int] = zc_embedding
        self.comments: Optional[str] = comments

    def __str__(self):
        return f'{self.index}-{self.word}({self.begin}:{self.end})({len(self.hits)})'

    def __repr__(self):
        return self.__str__()


QueryTuple = Tuple[str, str]  # (query_id, utt_id)
SynTree = Union[ET._Element, str]  # lxml etree or string representation
SastaMatch = Tuple[Match, SynTree]  # (matched part of the tree, whole tree)
SastaMatchList = List[SastaMatch]
SastaMatches = Dict[QueryTuple, SastaMatchList]
SastaResults = Dict[str, Counter[str]]  # {query_id: Counter({utt_id: num_matches, ..}, ..)
SastaAnnotations = Dict[str, List[UtteranceWord]]
SastaExactResults = Dict[str, List[Tuple[Union[str, int], int]]]  # exactresults: {query_id: [(utt_id, match_word_begin+1), ..], ..}
SastaAllUtts = Dict[str, List[str]]  # allutts : {utt_id: ['word1', 'word2', ..], ..}


class AllResults:
    """Query results and annotations of a single transcript

    Attributes
    ----------
    filename: str
        Transcript name. Does not need to be a complete filepath.
    uttcount: int
        Total number of utterances.
    coreresults: dict
        Results of pre and core queries, grouped by query.
    exactresults: dict
        Results, grouped by query
    postresults: dict
        Results of post queries, grouped by query.
    allmatches: dict
        All matched queries with the matched xml nodes.
    annotations: dict
        All annotations for the transcript, grouped by utterance.
    analysedtrees: list
        Syntactic trees (xml) for all utterances.
    annotationinput: bool
        Read annotations from SAF-file rather then generate from transcript.
    allutts: dict
        Dictionary with keys str(utt_id) and values list of words
    """

    def __init__(self,
                 filename,
                 uttcount,
                 coreresults=None,
                 exactresults=None,
                 postresults=None,
                 allmatches=None,
                 annotations=None,
                 analysedtrees=None,
                 annotationinput=None,
                 allutts=None):
        self.filename: str = filename
        self.uttcount: int = uttcount
        self.coreresults: SastaResults = coreresults or {}
        self.exactresults: SastaExactResults = exactresults or {}
        self.postresults: SastaResults = postresults or {}
        self.allmatches: SastaMatches = allmatches or tuple()
        self.annotations: SastaAnnotations = annotations or {}
        self.analysedtrees: List[SynTree] = analysedtrees or []
        self.annotationinput: bool = annotationinput or False
        self.allutts: SastaAllUtts = allutts or None

    def __repr__(self):
        return f'name: {self.filename}, core: {len(self.coreresults)}, post: {len(self.postresults)}, matches: {len(self.allmatches)}'


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
