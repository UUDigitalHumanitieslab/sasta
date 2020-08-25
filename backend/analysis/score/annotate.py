from analysis.results.results import AllResults
from analysis.models import Transcript, Utterance, AssessmentMethod
from typing import List, Set
from analysis.score.query import QueryWithFunction

import logging
logger = logging.getLogger('sasta')


def annotate_transcript(transcript: Transcript,
                        method: AssessmentMethod,
                        only_include_inform: bool,
                        calculate_zc_embeddings: bool):
    from analysis.score.run_queries import (
        filter_queries)
    from analysis.score.query import (
        compile_queries)
    # logger.info(f'Annotating {transcript.name}')

    queries = filter_queries(method)
    queries_with_funcs = compile_queries(queries)

    utterances = Utterance.objects.filter(transcript=transcript)

    allresults = AllResults(
        filename=transcript.content.name, uttcount=len(utterances))

    # logger.info(f'Succes, annotated {transcript.name}')
    print(allresults.coreresults)
    annotations, levels = core_queries(utterances,
                                       queries_with_funcs,
                                       allresults,
                                       only_include_inform,
                                       calculate_zc_embeddings)


def core_queries(utterances: List[Utterance],
                 queries_with_funcs: List[QueryWithFunction],
                 allresults: AllResults,
                 only_include_inform: bool,
                 calculate_zc_embeddings: bool):
    from analysis.score.run_queries import (
        utt_from_tree, single_query_single_utt)

    levels: Set[str] = set([])
    results = {}

    for utt in utterances:
        utt_res = utt_from_tree(utt.parse_tree, calculate_zc_embeddings)

        for q in queries_with_funcs:
            matches = single_query_single_utt(q.function, utt)
            if matches:
                for m in matches:
                    inform = q.query.inform if only_include_inform else True
                    if q.query.original and inform:
                        begin = int(m.get('begin'))
                        hit = {
                            'level': q.query.level,
                            'item': q.query.item,
                            'fase': q.query.fase
                        }
                        levels.add(q.query.level)
                        utt_res[begin].hits.append(hit)
                        # return corematches, coreresults, levels
        results[utt.utt_id] = utt_res
    return results, levels


# def v2_results(transcript, method, utterances,
#                queries_with_funcs, only_include_inform, zc_embeddings):
#     from analysis.score.run_queries import (
#         utt_from_tree, single_query_single_utt)
#     # match aggregate, grouped by utterance
#     results = {
#         'transcript': transcript.name,
#         'method': method.name,
#         'levels': set([]),
#         'results': {}
#     }
#     for utt in utterances:
#         utt_res = []
#         utt_res = utt_from_tree(utt.parse_tree, zc_embeddings)

#         for q in queries_with_funcs:
#             q_res = single_query_single_utt(q['q_func'], utt)
#             for res in q_res:
#                 if q['q_obj'].original and (
#                         q['q_obj'].inform if only_include_inform else True):
#                     res_begin = int(res.get('begin'))
#                     hit = {
#                         'level': q['q_obj'].level,
#                         'item': q['q_obj'].item,
#                         'fase': q['q_obj'].fase,
#                     }
#                     results['levels'].add(q['q_obj'].level)
#                     utt_res[res_begin].hits.append(hit)
#         results['results'][utt.utt_id] = utt_res
#     return results
