import operator
from collections import Counter, defaultdict
from functools import reduce
from typing import Dict, List, Optional

from analysis.models import AssessmentMethod
from analysis.results.results import (AllResults, SastaAllUtts, SastaAnnotations, SastaExactResults,
                                      UtteranceWord)


class SAFAnnotation:
    def __init__(self, level, label, fase=None, query_id=None):
        self.level: str = level
        self.label: str = label
        self.fase: str = fase
        self.query_id: Optional[str] = query_id


class SAFDocument:
    def __init__(self, name, method, all_levels=None):
        self.name: str = name
        self.method: AssessmentMethod = method
        self.utterances: List[SAFUtterance] = []
        self.all_levels: Optional[List[str]] = all_levels
        self.annotations: SastaAnnotations = {}
        self.exactresults: SastaExactResults = defaultdict(list)
        self.allutts: SastaAllUtts = defaultdict(list)

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

    def to_allresults(self) -> AllResults:
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
            coreresults=results,
            exactresults=self.exactresults,
            allutts=self.allutts
        )

        return allresults

    @property
    def reformatted_annotations(self) -> Dict[int, List[UtteranceWord]]:
        annotations = {}
        for utt in self.utterances:
            annotations[utt.utt_id] = []
            for word in utt.words:
                uw = UtteranceWord(
                    word=word.text,
                    begin=word.idx - 1,  # TODO: does this need to be normalized?
                    end=word.idx,
                    hits=[],
                    idx=word.idx,
                    zc_embedding=0,  # TODO: CHECK ZC EMBEDS,
                    comments=word.comment
                )
                for ann in word.annotations:
                    hit = self.hit_from_annotation(ann)
                    uw.hits.append(hit)
                annotations[utt.utt_id].append(uw)
        return annotations

    def hit_from_annotation(self, ann) -> Dict:
        q = self.method.queries.get(query_id=ann.query_id)
        # Try to match the actual alt item
        item_matches = [ai for ai in q.altitems if ai.lower() == ann.label.lower()]
        return {
            'level': q.level,
            'item': item_matches[0] if item_matches else q.item,
            'fase': q.fase
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
    def __init__(self, idx, text, begin, end, comment=None):
        self.idx: int = idx
        self.begin: int = begin
        self.end: int = end
        self.text: str = text
        self.annotations: List[SAFAnnotation] = []
        self.comment: str = comment or ''

    @property
    def item_counts(self):
        return Counter({a.query_id for a in self.annotations if a.query_id})
