from typing import Union

from lxml import etree as ET

from ..models import AssessmentMethod, AssessmentQuery, Transcript

from django.db.models import Q

from copy import deepcopy

import subprocess


def compile_xpath_or_func(query: str) -> Union[ET.XPath, None]:
    try:
        return ET.XPath(query)
    except ET.XPathEvalError:
        return None
    except ET.XPathSyntaxError as e:
        print(e, query)
        return None


def query_transcript(transcript: Transcript, method: AssessmentMethod, phase=2, phase_exact=True):
    queries = filter_queries(method, phase, phase_exact=False)
    queries_with_funcs = compile_queries(queries)
    query_single_transcript(transcript, queries_with_funcs)

    pass


def filter_queries(method: AssessmentMethod, phase: int = None, phase_exact: bool = True):
    '''
    phase_exact:   True returns only that phase
                    False returns everything up to that phase (e.g. for 3 -> 1,2,3)
    '''
    try:
        all_queries = AssessmentQuery.objects.filter(
            Q(method=method) & Q(query__isnull=False))
        phase_filter = Q(phase=phase) if phase_exact else Q(phase__gte=phase)
        queries = all_queries.filter(phase_filter)
        return queries
    except Exception as e:
        # TODO: log
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
        # TODO log
        return None


def query_single_transcript(transcript: Transcript, queries_with_funcs):
    with open(transcript.parsed_content.path, 'rb') as f_in:
        doc = ET.fromstring(f_in.read())
        utterances = doc.xpath('.//alpino_ds')
        with open('logs/score.log', 'w') as f_out:
            for utt in utterances:
                copied_utt = deepcopy(utt)
                sent = copied_utt.xpath('sentence')[0].text.replace('\n', '')
                xsid = copied_utt.xpath('//meta[@name="xsid"]')
                print(sent, file=f_out)
                for query in queries_with_funcs:
                    q_res = run_single_query(query['q_func'], copied_utt)
                    if q_res:
                        print(query['q_id'], '\t', len(q_res), file=f_out)
