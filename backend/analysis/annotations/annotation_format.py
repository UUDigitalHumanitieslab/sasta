import operator
from collections import Counter
from functools import reduce
from typing import List, Optional

from analysis.results.results import AllResults


class SAFAnnotation:
    def __init__(self, level, label, fase=None, query_id=None):
        self.level: str = level
        self.label: str = label
        self.fase: str = fase
        self.query_id: Optional[str] = query_id


class SAFDocument:
    def __init__(self, name, method_name='', all_levels=None):
        self.name: str = name
        self.method_name: str = method_name
        self.utterances: List[SAFUtterance] = []
        self.all_levels: Optional[List[str]] = all_levels

    @property
    def all_annotations(self):
        return reduce(operator.concat,
                      [utt.annotations for utt in self.utterances])

    @property
    def queries(self):
        '''Set of all query IDs in the document'''
        return set(
            ann.query_id for ann in self.all_annotations
        )

    @property
    def item_counts(self):
        return {u.utt_id: u.item_counts for u in self.utterances}

    def to_allresults(self):
        '''Convert to AllResults object (for query and scoring).'''
        filename = self.name
        uttcount = len(self.utterances)
        results = {
            q: Counter({
                u.utt_id: u.item_counts[q]
                for u in self.utterances
                if u.item_counts[q] > 0
            })
            for q in self.queries
        }

        allresults = AllResults(
            filename,
            uttcount,
            coreresults=results
        )

        return allresults


class SAFUtterance:
    def __init__(self, utt_id):
        self.utt_id: int = utt_id
        self.words: List[SAFWord] = []

    @property
    def item_counts(self):
        return sum([w.item_counts for w in self.words], Counter())

    @property
    def annotations(self):
        return reduce(operator.concat, [w.annotations for w in self.words])


class SAFWord:
    def __init__(self, idx, text):
        self.idx: int = idx
        self.text: str = text
        self.annotations: List[SAFAnnotation] = []

    @property
    def item_counts(self):
        return Counter({a.query_id for a in self.annotations if a.query_id})
