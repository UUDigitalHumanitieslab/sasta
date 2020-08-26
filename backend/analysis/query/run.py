import logging
from typing import List, Set
from collections import defaultdict, Counter

from analysis.models import (AssessmentMethod, AssessmentQuery, Transcript,
                             Utterance)
from analysis.query.functions import (QueryWithFunction, compile_queries,
                                      filter_queries)
from analysis.results.results import AllResults, SastaMatches, SastaResults
from analysis.query.functions import single_query_single_utt

logger = logging.getLogger('sasta')


def query_transcript(transcript: Transcript, method: AssessmentMethod):
    # TODO: LOGGING

    queries: List[AssessmentQuery] = filter_queries(method)
    queries_with_funcs: List[QueryWithFunction] = compile_queries(queries)
    utterances: List[Utterance] = Utterance.objects.filter(
        transcript=transcript)

    coreresults, allmatches, corelevels = core_queries(
        utterances,
        queries_with_funcs,
        only_include_inform=False,
        generate_zc_embeddings=False,
        generate_annotations=False)
    # postresults = post_queries()

    allresults = AllResults(transcript.name, len(
        utterances), coreresults, None, allmatches, None)
    return coreresults


def core_queries(utterances: List[Utterance],
                 queries: List[QueryWithFunction],
                 only_include_inform: bool,
                 generate_zc_embeddings: bool,
                 generate_annotations: bool):
    # TODO: annotations
    levels: Set[str] = set([])
    allmatches: SastaMatches = defaultdict(list)
    results: SastaResults = {}

    for utt in utterances:
        for q in queries:
            matches = single_query_single_utt(q.function, utt.syntree)
            if matches:
                if q.id in results:
                    results[q.id].update(
                        {utt.utt_id: len(matches), 'total': len(matches)})
                else:
                    results[q.id] = Counter(
                        {utt.utt_id: len(matches), 'total': len(matches)})
                for m in matches:
                    levels.add(q.query.level)
                    allmatches[(q.id, utt.utt_id)].append((m, utt.syntree))

    return results, matches, levels

    # annotations = {}

    # for utt in utterances:
    # utt_res = utt_from_tree(utt.parse_tree, calculate_zc_embeddings)
    # for q in queries_with_funcs:
    #     matches = single_query_single_utt(q.function, utt.syntree)
    #     for m in matches:
    #         levels.add(q.query.level)

    #                 inform = q.query.inform if only_include_inform else True
    #                 if q.query.original and inform:
    #                     begin = int(m.get('begin'))
    #                     hit = {
    #                         'level': q.query.level,
    #                         'item': q.query.item,
    #                         'fase': q.query.fase
    #                     }
    #                     utt_res[begin].hits.append(hit)
    #     annotations[utt.utt_id] = utt_res
    # return annotations, levels
    # return levels
    # return coreresults, corematchers, corelevels
    # for utt in utterances:
    #         single_q_res = single_query_single_utt(query_with_func['q_func'], utt)
    #         if single_q_res:
    #             # count the hits for v1 results
    #             query_counter['total'] += len(single_q_res)
    #             query_counter[utt.utt_id] += len(single_q_res)

    #     return (query_counter, query_results) or None


def annotate_transcript(transcript: Transcript,
                        method: AssessmentMethod,
                        only_include_inform: bool,
                        calculate_zc_embeddings: bool):
    # TODO: LOGGING

    queries = filter_queries(method)
    queries_with_funcs = compile_queries(queries)

    utterances = Utterance.objects.filter(transcript=transcript)

    allresults = AllResults(
        filename=transcript.content.name, uttcount=len(utterances))

    # coreresults, levels = core_queries(utterances,
    #                                    queries_with_funcs,
    #                                    allresults,
    #                                    only_include_inform,
    #                                    calculate_zc_embeddings,
    #                                    generate_annotations=True)

    # print(coreresults)
