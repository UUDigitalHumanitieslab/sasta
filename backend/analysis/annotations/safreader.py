import logging
import os
from typing import List, Optional, Tuple

import pandas as pd
from analysis.models import Transcript

from .annotation_format import (SAFAnnotation, SAFDocument, SAFUtterance,
                                SAFWord)
from .constants import LABELSEP, PREFIX, SAF_COMMENT_LEVEL, UTTLEVEL
from .utils import (clean_item, clean_row, enrich, getlabels,
                    item2queryid, mkpatterns, standardize_header_name)

logger = logging.getLogger('sasta')


def get_word_levels(data: pd.DataFrame):
    levels = data.level
    filtered_levels = levels[~levels.isin([SAF_COMMENT_LEVEL.lower(), UTTLEVEL.lower()])]
    return list(filtered_levels.unique())


def is_word_column(column_name: str) -> bool:
    return column_name.lower().startswith('word') or column_name.lower() == 'unaligned'


class SAFReader:
    def __init__(self, filepath, method, transcript: Transcript = None):
        self.filepath = filepath
        self.word_cols = []
        self.levels: List[str] = []
        self.data = self.loaddata(filepath)
        self.method = method
        self.transcript: Optional[Transcript] = transcript or None
        self.item_mapping, self.patterns = self.make_mappings()
        self.document = SAFDocument(os.path.basename(
            filepath), method, self.levels)
        self.errors: List[Tuple] = []
        self.get_annotations(self.data)

    def formatted_errors(self):
        results = []
        for (utt_id, word_id, text, level, label) in self.errors:
            results.append(f'Unknown item "{label}" found in utterance {utt_id}, word {word_id} ("{text}"), level "{level}"')
        return results

    def loaddata(self, filepath):
        data = pd.read_excel(filepath)
        data.rename(columns=standardize_header_name, inplace=True)
        data = data.where(data.notnull(), None)
        data.dropna(how='all', axis=1, inplace=True)
        self.word_cols = list(filter(is_word_column, data.columns))

        relevant_cols = ['utt_id', 'level'] + self.word_cols
        self.levels = [lv for lv in list(
            data.level.dropna().unique()) if lv.lower() != UTTLEVEL]

        data = data[relevant_cols].apply(clean_row, axis='columns')

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
        utt_object = self.transcript.get_utterance_by_id(utt_id)
        self.document.allutts[utt_object.utt_id] = utt_object.word_list
        for idx, wcol in enumerate(self.word_cols):
            relevant_cols = ['level', wcol]
            word = self.parse_word(utt_id, idx,
                                   wcol, utt_data[relevant_cols], utt_object.word_position_mapping)
            if word:
                instance.words.append(word)

        return instance

    def parse_word(self, utt_id, word_id, colname, word_data, wordposmap):
        data = word_data.dropna()
        if data.empty:
            return None
        utt_data = data.loc[data.level == UTTLEVEL, colname]
        if utt_data.empty:
            return None
        text = utt_data.iloc[0]
        text = data.loc[data.level == UTTLEVEL, colname].iloc[0]
        (begin, end) = wordposmap[word_id]['begin'], wordposmap[word_id]['end']
        instance = SAFWord(word_id, text, begin, end)

        word_levels = get_word_levels(data)
        for level in word_levels:
            label = clean_item(data.loc[data.level == level, colname].iloc[0])
            enriched_label = enrich(label, PREFIX.lower())
            split_labels = getlabels(enriched_label, self.patterns)

            if not split_labels:
                self.errors.append((utt_id, word_id, text, level, label))

            for label in split_labels:
                mapped = item2queryid(label, level, self.item_mapping)
                if mapped:
                    query_id, fase = mapped
                    instance.annotations.append(SAFAnnotation(
                        level, label, fase, query_id))
                    self.document.exactresults[query_id].append((utt_id, word_id))

                else:
                    logger.warning(
                        'Cannot resolve query_id for (%s, %s)', level, label)
                    self.errors.append((utt_id, word_id, text, level, label))

        # read comments
        comment_data = data.loc[data.level == SAF_COMMENT_LEVEL.lower()]
        if not comment_data.empty:
            instance.comment = str(comment_data[colname].iloc[0])

        return instance
