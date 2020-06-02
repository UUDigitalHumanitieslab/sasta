from typing import List, Optional, Set
from collections import Counter
import operator
from functools import reduce


class SAFAnnotation:
    def __init__(self, level, label, query_id=None):
        self.level: str = level
        self.label: str = label
        self.query_id: Optional[str] = query_id


class SAFDocument:
    def __init__(self, name, method_name='', all_levels=None):
        self.name: str = name
        self.method_name: str = method_name
        self.utterances: List[SAFUtterance] = []
        self.all_levels: Optional[List[str]] = all_levels

    @property
    def all_annotations(self):
        return reduce(operator.concat, [utt.annotations for utt in self.utterances])

    @property
    def item_counts(self):
        return {u.utt_id: u.item_counts for u in self.utterances}

    @property
    def results(self):
        return {
            'transcript': self.name,
            'method': self.method_name,
            'levels': self.all_levels,
            'results': self.item_counts
        }


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
