from ..utils import v1_to_xlsx
from collections import Counter
from typing import Union

from django.db.models import Q
from lxml import etree as ET

from ..models import AssessmentMethod, AssessmentQuery, Transcript, Utterance

import logging
logger = logging.getLogger('sasta')


def compile_xpath_or_func(query: str) -> Union[ET.XPath, None]:
    try:
        return ET.XPath(query)
    except ET.XPathEvalError as error:
        # TODO: python functions
        logger.warning(f'cannot compile {query.strip()}:\t{error}')
        return None
    except Exception as error:
        logger.warning(f'cannot compile {query.strip()}:\t{error}')
        return None


def compile_queries(queries):
    query_funcs = []
    for q in queries:
        func = compile_xpath_or_func(q.query)
        query_funcs.append({'q_id': q.query_id, 'q_obj': q, 'q_func': func})
    return query_funcs


def query_transcript(transcript: Transcript, method: AssessmentMethod):
    logger.info(f'Start querying {transcript.name}')

    queries = filter_queries(method)
    queries_with_funcs = compile_queries(queries)

    utterances = Utterance.objects.filter(transcript=transcript)

    v1_results = {
        'transcript': transcript.name,
        'method': method.name,
        'results': {}
    }

    for q in queries_with_funcs:
        query_res = single_query_single_transcript(q, utterances)
        if query_res:
            v1_results['results'][q['q_id']] = query_res
    return v1_results


def single_query_single_transcript(query_with_func, utterances):
    # run a single query over every utterance
    # return: counter with utt_ids and counts
    query_counter = Counter()
    for utt in utterances:
        results = single_query_single_utt(query_with_func['q_func'], utt)
        if results:
            query_counter[utt.utt_id] += results
            # query_counter.update(utt.utt_id)
    return query_counter or None


def single_query_single_utt(query_func, utt_obj):
    # run a single query against a single utterance
    # return list of matches
    try:
        results = query_func(ET.fromstring(utt_obj.parse_tree))
        return len(results)
    except Exception as e:
        logger.warning(f'Failed to execute {query_func}')


def filter_queries(method: AssessmentMethod, phase: int = None, phase_exact: bool = True):
    '''
    # TODO: remove?
    phase_exact:   True returns only that phase
                    False returns everything up to that phase (e.g. for 3 -> 1,2,3)
    '''
    try:
        all_queries = AssessmentQuery.objects.filter(
            Q(method=method) & Q(query__isnull=False))
        if phase:
            phase_filter = Q(phase=phase) if phase_exact else Q(
                phase__gte=phase)
            phase_queries = all_queries.filter(phase_filter)
            return phase_queries
        return all_queries

    except Exception as e:
        logger.warning(f'cannot filter queries for phase:\t{e}')
        print(e)
