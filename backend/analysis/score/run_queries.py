import logging
from collections import Counter
from operator import attrgetter
from typing import List, Union

from bs4 import BeautifulSoup as Soup
from django.db.models import Q
from lxml import etree as ET

from ..models import AssessmentMethod, AssessmentQuery, Transcript, Utterance
from . import external_functions

logger = logging.getLogger('sasta')


class UtteranceWord:
    def __init__(self, word: str, begin: int, end: int, hits: List[str]):
        self.word = word
        self.begin = begin
        self.end = end
        self.hits = hits

    def __str__(self):
        return f'{self.word}({self.begin}:{self.end})({len(self.hits)})'

    def __repr__(self):
        return self.__str__()


def utt_from_tree(tree: str):
    # From a LASSY syntax tree, construct utterance representation
    # Output: sorted list of UtteranceWord instances
    soup = Soup(tree, 'lxml')
    utt = soup.alpino_ds

    words = utt.findAll('node', {'word': True})
    utt_words = [UtteranceWord(w.get('word'), w.get(
        'begin'), w.get('end'), []) for w in words]

    return sorted(utt_words, key=attrgetter('begin'))


def compile_xpath_or_func(query: str) -> Union[ET.XPath, None]:
    try:
        if query in dir(external_functions):
            return getattr(external_functions, query)
        return ET.XPath(query)
    except Exception as error:
        logger.warning(f'cannot compile {query.strip()}:\t{error}')
        return None


def compile_queries(queries):
    query_funcs = []
    for q in queries:
        func = compile_xpath_or_func(q.query)
        query_funcs.append({'q_id': q.query_id, 'q_obj': q, 'q_func': func})
    return query_funcs


def annotate_transcript(transcript: Transcript, method: AssessmentMethod):
    logger.info(f'Annotating {transcript.name}')
    queries = filter_queries(method)
    queries_with_funcs = compile_queries(queries)
    utterances = Utterance.objects.filter(transcript=transcript)

    results = v2_results(transcript, method, utterances, queries_with_funcs)
    # spreadsheet = v2_to_xlsx(v2)

    logger.info(f'Succes, annotated {transcript.name}')
    return results


def query_transcript(transcript: Transcript, method: AssessmentMethod):
    logger.info(f'Start querying {transcript.name}')

    queries = filter_queries(method)
    queries_with_funcs = compile_queries(queries)

    utterances = Utterance.objects.filter(transcript=transcript)

    v1 = v1_results(transcript, method, utterances, queries_with_funcs)
    # v1_to_xlsx(v1_results, '/Users/3248526/Documents/v1_test.xlsx')

    v2 = v2_results(transcript, method, utterances, queries_with_funcs)
    # v2_to_xlsx(v2, '/Users/3248526/Documents/v2_test.xlsx')

    logger.info(f'Succes querying {transcript.name}')
    return v1


def v1_results(transcript, method, utterances, queries_with_funcs):
    # simple counts aggregate, grouped by query
    results = {
        'transcript': transcript.name,
        'method': method.name,
        'results': {}
    }

    for q in queries_with_funcs:
        query_res = single_query_single_transcript(q, utterances)
        if query_res:
            results['results'][q['q_id']] = {
                'id': q['q_id'],
                'item': q['q_obj'].item,
                'fase': q['q_obj'].fase or 0,
                'matches': query_res[0]
            }
    return results


def v2_results(transcript, method, utterances, queries_with_funcs):
    # match aggregate, grouped by utterance
    results = {
        'transcript': transcript.name,
        'method': method.name,
        'levels': set([]),
        'results': {}
    }
    for utt in utterances:
        utt_res = []
        utt_res = utt_from_tree(utt.parse_tree)

        for q in queries_with_funcs:
            q_res = single_query_single_utt(q['q_func'], utt)
            for res in q_res:
                if q['q_obj'].original and q['q_obj'].inform:
                    res_begin = int(res.get('begin'))
                    hit = {
                        'level': q['q_obj'].level,
                        'item': q['q_obj'].item,
                        'fase': q['q_obj'].fase
                    }
                    results['levels'].add(q['q_obj'].level)
                    utt_res[res_begin].hits.append(hit)
        results['results'][utt.utt_id] = utt_res
    return results


def single_query_single_transcript(query_with_func, utterances):
    # run a single query over every utterance
    # return: counter with utt_ids and counts
    query_counter = Counter()
    query_results = []

    for utt in utterances:
        single_q_res = single_query_single_utt(query_with_func['q_func'], utt)
        if single_q_res:
            # count the hits for v1 results
            query_counter['total'] += len(single_q_res)
            query_counter[utt.utt_id] += len(single_q_res)

            # record hits (begin position) for v2 results
            query_results.append({
                'utt_id': utt.utt_id,
                'hits': [res.get('begin') for res in single_q_res]
            })

    return (query_counter, query_results) or None


def single_query_single_utt(query_func, utt_obj):
    # run a single query against a single utterance
    # return list of matches
    try:
        results = query_func(ET.fromstring(utt_obj.parse_tree))
        return results
    except Exception:
        logger.warning(f'Failed to execute {query_func}')


def filter_queries(method: AssessmentMethod, phase: int = None, phase_exact: bool = True):
    '''
    # TODO: remove?
    phase_exact:   True returns only that phase
                    False returns everything up to that phase (e.g. for 3 -> 1,2,3)
    '''
    try:
        all_queries = AssessmentQuery.objects.all().filter(
            Q(method=method) & Q(query__isnull=False))
        if phase:
            phase_filter = Q(fase=phase) if phase_exact else Q(
                fase__gte=phase)
            phase_queries = all_queries.filter(phase_filter)
            return phase_queries
        return all_queries

    except Exception as e:
        logger.warning(f'cannot filter queries for phase:\t{e}')
        print(e)
