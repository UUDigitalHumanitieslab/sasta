import logging
import os
from typing import List, Optional, Tuple

import pandas as pd
from analysis.models import Transcript
from annotations.constants import (SAF_COMMENT_HEADERS, SAF_UNALIGNED_LEVEL,
                                   SAF_UNALIGNED_LEVELS, SAF_UTT_HEADER,
                                   SAF_UTT_LEVELS)

from .annotation_format import (SAFAnnotation, SAFDocument, SAFUtterance,
                                SAFWord)
from .constants import LABELSEP, PREFIX
from .utils import (clean_item, clean_row, enrich, getlabels, item2queryid,
                    mkpatterns, standardize_header_name)

logger = logging.getLogger('sasta')


class NoWordDataException(Exception):
    '''Raised when:
    - There are no annotations for the word/level combination OR
    - There is no word
    '''
    pass


class UnalignedWord(Exception):
    '''Raised when word is unaligned'''
    pass


def get_word_levels(data: pd.DataFrame):
    levels = data.level
    filtered_levels = levels[~levels.isin(
        [*SAF_COMMENT_HEADERS, *SAF_UTT_LEVELS])]
    return list(filtered_levels.unique())


def is_word_column(column_name: str) -> bool:
    return column_name.lower().startswith('word')


def word_level_data(word_data: pd.DataFrame, colname: str):
    '''returns combination word/level
    '''
    if colname.lower() in SAF_UNALIGNED_LEVELS:
        raise UnalignedWord
    elif word_data.empty:
        raise NoWordDataException
    utt_data = word_data.loc[word_data.level.isin(SAF_UTT_LEVELS), colname]
    return utt_data


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
        data = pd.read_excel(filepath, engine='openpyxl')
        data.rename(columns=standardize_header_name, inplace=True)
        data = data.where(data.notnull(), None)
        self.word_cols = [SAF_UNALIGNED_LEVEL.lower()] + \
            list(filter(is_word_column, data.columns))

        # Do we need to drop empty columns? Seems we don't. If otherwise, make sure word_columns are not dropped
        # data.dropna(how='all', axis=1, inplace=True)

        relevant_cols = [
            *SAF_UTT_LEVELS,
            'level',
            *SAF_UNALIGNED_LEVELS,
            *self.word_cols
        ]
        to_clean_cols = [col for col in set(
            relevant_cols) if col in data.columns]
        self.levels = [lv for lv in list(
            data.level.dropna().unique()) if lv.lower() not in SAF_UTT_LEVELS]

        data = data[to_clean_cols].apply(clean_row, axis='columns')

        return data

    def make_mappings(self):
        item_mapping = self.method.get_item_mapping(LABELSEP)
        items = [item for (item, _) in item_mapping if item]
        patterns = mkpatterns(items)
        return item_mapping, patterns

    def get_annotations(self, data):
        for utt_id in data[SAF_UTT_HEADER.lower()].unique():
            utt_rows = data[data[SAF_UTT_HEADER.lower()] == utt_id]
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
        data = word_data
        if colname != SAF_UNALIGNED_LEVEL.lower():
            # Don't drop data for unaligned
            data = word_data.dropna()

        try:
            utt_data = word_level_data(data, colname)
            text = utt_data.iloc[0]

        except UnalignedWord:
            text = ''
        except NoWordDataException:
            return None

        (begin, end) = wordposmap[word_id]['begin'], wordposmap[word_id]['end']
        instance = SAFWord(word_id, text, begin, end)

        word_levels = get_word_levels(data)
        for level in word_levels:
            item_data = data.loc[data.level == level, colname].iloc[0]
            if not pd.isnull(item_data):
                label = clean_item(item_data)
                enriched_label = enrich(label, PREFIX.lower())
                split_labels = getlabels(enriched_label, self.patterns)

                if not split_labels:
                    self.errors.append((utt_id, word_id, text, level, label))

                self.map_labels(split_labels, instance,
                                level, utt_id, word_id, text)

        # read comments
        comment_data = data.loc[data.level.isin(SAF_COMMENT_HEADERS)].dropna()
        if not comment_data.empty:
            instance.comment = str(comment_data[colname].iloc[0])

        return instance

    def map_labels(self, split_labels: List[str], saf_word: SAFWord, level: str, utt_id, word_id, text):
        for label in split_labels:
            mapped = item2queryid(label, level, self.item_mapping)
            if mapped:
                query_id, fase = mapped
                saf_word.annotations.append(SAFAnnotation(
                    level, label, fase, query_id))
                self.document.exactresults[query_id].append(
                    (utt_id, word_id))

            else:
                logger.warning(
                    'Cannot resolve query_id for (%s, %s)', level, label)
                self.errors.append(
                    (utt_id, word_id, text, level, label))
