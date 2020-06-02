from pprint import pprint
import logging
import os

import pandas as pd

from .annotation_format import (SAFAnnotation, SAFDocument, SAFUtterance,
                                SAFWord)
from .config import LABELSEP, PREFIX, UTTLEVEL
from .utils import (clean_cell, enrich, getlabels, item2queryid, mkpatterns,
                    standardize_header_name)
from typing import List

logger = logging.getLogger('sasta')


class SAFReader:
    def __init__(self, filepath, method):
        # self.filepath = filepath
        filepath = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'test_sample.xlsx')
        self.word_cols = []
        self.levels: List[str] = []
        self.data = self.loaddata(filepath)
        self.method = method
        self.item_mapping, self.patterns = self.make_mappings()
        self.document = SAFDocument(os.path.basename(
            filepath), method.name, self.levels)
        self.get_annotations(self.data)

        pprint(self.document.results)

    def loaddata(self, filepath):
        data = pd.read_excel(filepath)
        data.rename(columns=standardize_header_name, inplace=True)
        data = data.where(data.notnull(), None)
        data.dropna(how='all', axis=1, inplace=True)
        self.word_cols = [c for c in data.columns if c.startswith('word')]
        relevant_cols = ['utt_id', 'level'] + self.word_cols
        self.levels = [l for l in list(
            data.level.unique()) if l.lower() != UTTLEVEL]
        data = data[relevant_cols].applymap(clean_cell)
        return data

    def make_mappings(self):
        item_mapping = self.method.get_item_mapping(LABELSEP)
        items = [item for (item, _) in item_mapping if item]
        patterns = mkpatterns(items)
        return item_mapping, patterns

    def get_annotations(self, data):
        for utt_id in data.utt_id.unique():
            utt_rows = data[data.utt_id == utt_id]
            parsed_utterance = self.parse_utterance(utt_id, utt_rows)
            self.document.utterances.append(parsed_utterance)

    def parse_utterance(self, utt_id, utt_data):
        instance = SAFUtterance(utt_id)
        for idx, wcol in enumerate(self.word_cols):
            relevant_cols = ['level', wcol]
            word = self.parse_word(idx+1,
                                   wcol, utt_data[relevant_cols])
            if word:
                instance.words.append(word)
        return instance

    def parse_word(self, word_id, colname, word_data):
        data = word_data.dropna()
        if data.empty:
            return None
        text = data.loc[data.level == UTTLEVEL, colname].iloc[0]
        instance = SAFWord(word_id, text)

        word_levels = [l for l in data.level.unique() if l != UTTLEVEL]
        for level in word_levels:
            label = data.loc[data.level == level, colname].iloc[0]
            enriched_label = enrich(label, PREFIX.lower())
            split_labels = getlabels(enriched_label, self.patterns)

            for label in split_labels:
                query_id = item2queryid(label, level, self.item_mapping)
                if query_id:
                    instance.annotations.append(SAFAnnotation(
                        level, label, query_id))
                else:
                    logger.warning(
                        'Cannot resolve query_id for (%s, %s)', level, label)
        return instance
