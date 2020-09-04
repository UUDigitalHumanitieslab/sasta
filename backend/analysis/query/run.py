from analysis.query.xlsx_output import v1_to_xlsx
import logging
from collections import Counter, defaultdict
from pprint import pprint
from typing import Dict, List, Set

from analysis.config import CORE_PROCESS, POST_PROCESS
from analysis.models import (AssessmentMethod, AssessmentQuery, Transcript,
                             Utterance)
from analysis.query.functions import (Query, QueryWithFunction,
                                      compile_queries, filter_queries,
                                      single_query_single_utt)
from analysis.results.results import AllResults, SastaMatches, SastaResults

logger = logging.getLogger('sasta')


def query_transcript(transcript: Transcript, method: AssessmentMethod):
    # TODO: LOGGING

    queries: List[AssessmentQuery] = filter_queries(method)
    queries_with_funcs: List[QueryWithFunction] = compile_queries(queries)
    utterances: List[Utterance] = Utterance.objects.filter(
        transcript=transcript)

    coreresults, allmatches, corelevels = run_core_queries(
        utterances,
        queries_with_funcs,
        only_include_inform=False,
        generate_zc_embeddings=False,
        generate_annotations=False)

    allresults = AllResults(transcript.name, len(
        utterances), coreresults, None, allmatches, None)

    run_post_queries(allresults, queries_with_funcs)
    # pprint(allresults.coreresults)
    # print('------------')
    # pprint(allresults.postresults)
    v1_to_xlsx(allresults, queries_with_funcs)
    return allresults, queries_with_funcs


def run_core_queries(utterances: List[Utterance],
                     queries: List[QueryWithFunction],
                     only_include_inform: bool,
                     generate_zc_embeddings: bool,
                     generate_annotations: bool):
    # TODO: annotations
    levels: Set[str] = set([])
    allmatches: SastaMatches = defaultdict(list)
    results: SastaResults = {}

    core_queries: List[QueryWithFunction] = [
        q for q in queries if q.query.process == CORE_PROCESS]

    for utt in utterances:
        for q in core_queries:
            matches = single_query_single_utt(q.function, utt.syntree)
            if matches:
                if q.id in results:
                    results[q.id].update(
                        # {utt.utt_id: len(matches), 'total': len(matches)})
                        {utt.utt_id: len(matches)})
                else:
                    results[q.id] = Counter(
                        # {utt.utt_id: len(matches), 'total': len(matches)})
                        {utt.utt_id: len(matches)})
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


def run_post_queries(allresults: SastaResults,
                     queries: List[QueryWithFunction]) -> None:
    post_queries: List[QueryWithFunction] = [
        q for q in queries if q.query.process == POST_PROCESS]
    flat_queries: Dict[str, Query] = {q.id: q.query for q in queries}

    for q in post_queries:
        try:
            result = q.function(allresults, flat_queries)
            if result:
                allresults.postresults[q.id] = result
        except Exception:
            logger.warning(f'Failed to execute {q.function}')


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
