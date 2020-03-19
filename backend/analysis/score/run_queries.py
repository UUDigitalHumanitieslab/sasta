from collections import OrderedDict
from copy import deepcopy
from typing import Union

from django.db.models import Q
from lxml import etree as ET

from ..models import AssessmentMethod, AssessmentQuery, Transcript

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


def query_transcript(transcript: Transcript, method: AssessmentMethod, phase=None, phase_exact=False):
    logger.info(f'Start querying {transcript.name}')
    queries = filter_queries(method, phase, phase_exact)
    queries_with_funcs = compile_queries(queries)

    by_utterance_results = query_single_transcript(
        transcript, method, queries_with_funcs)
    by_query_results = results_by_query(by_utterance_results)

    logger.info(f'Finished querying {transcript.name}')
    return by_utterance_results, by_query_results


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


def compile_queries(queries):
    query_funcs = []
    for q in queries:
        func = compile_xpath_or_func(q.query)
        query_funcs.append({'q_id': q.query_id, 'q_obj': q, 'q_func': func})
    return query_funcs


def run_single_query(query_func, utterance_tree):
    try:
        return query_func(utterance_tree)
    except Exception as e:
        logger.warning(f'cannot execute {query_func}:\t{e}')
        return None


def query_single_transcript(transcript: Transcript, method, queries_with_funcs):
    # TODO: replace OrderedDict with proper classes
    try:
        with open(transcript.parsed_content.path, 'rb') as f_in:
            doc = ET.fromstring(f_in.read())
            utterances = doc.xpath('.//alpino_ds')
            # aggregation of results for entire transcript, grouped on utterance
            transcript_results = OrderedDict({
                'transcript': transcript.name,
                'method': method.name,
                'utterances': []
            })

            for utt in utterances:
                copied_utt = deepcopy(utt)
                sent = copied_utt.xpath('sentence')[
                    0].text.replace('\n', '')
                xsid = copied_utt.xpath(
                    '//meta[@name="xsid"]')
                utt_id = '-'
                if xsid:
                    utt_id = xsid[0].attrib['value']

                # results for a single utterance
                utterance_result = OrderedDict({
                    'utt_id': utt_id,
                    'sentence': sent,
                    'hits': []
                })

                for query in queries_with_funcs:
                    query_results = run_single_query(
                        query['q_func'], copied_utt)
                    if query_results:
                        utterance_result['hits'].append((
                            query['q_id'], len(query_results)))
                if utterance_result['hits']:
                    transcript_results['utterances'].append(
                        utterance_result)

        return transcript_results

    except Exception as e:
        logger.warning(f'error querying {transcript.name}:\t{e}')
        return None


def results_by_query(input_results):
    try:
        # results for a transcript, grouped by query
        transcript_results = input_results.copy()
        by_utt_results = transcript_results.pop('utterances', None)
        transcript_results['queries'] = []

        query_results = {}

        for item in by_utt_results:
            # OrderedDict([('utt_id', '2'), ('sentence', 'innu kast'), ('hits', [('T147', 1)])])
            # query_results.append((item['utt_id']))
            for hit in item['hits']:
                if not hit[0] in query_results:
                    query_results[hit[0]] = []
                query_results[hit[0]].append(
                    (item['utt_id'], item['sentence'], hit[1]))

        for k in sorted(query_results.keys()):
            transcript_results['queries'].append(
                OrderedDict({
                    'query_id': k,
                    'hits': query_results[k]
                })
            )
        return(transcript_results)

    except Exception as error:
        logger.warning(f'cannot generate results per query:\t{error}')
        return None
