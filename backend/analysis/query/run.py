import logging
from collections import Counter, defaultdict
from typing import Dict, List, Set

from analysis.models import (AnalysisRun, AssessmentMethod, AssessmentQuery, Transcript,
                             Utterance)
from analysis.results.results import AllResults, SastaMatches, SastaResults
from sastadev.query import core_process, post_process
from analysis.annotations.safreader import SAFReader
from .functions import (Query, QueryWithFunction, compile_queries,
                        filter_queries, single_query_single_utt, utt_from_tree)

logger = logging.getLogger('sasta')


def query_transcript(transcript: Transcript,
                     method: AssessmentMethod,
                     annotate: bool = False,
                     zc_embed: bool = False):
    # TODO: LOGGING

    queries: List[AssessmentQuery] = filter_queries(method)
    queries_with_funcs: List[QueryWithFunction] = compile_queries(queries)
    utterances: List[Utterance] = Utterance.objects.filter(
        transcript=transcript)
    to_analyze_utterances = [x for x in utterances if x.for_analysis]
    logger.info(
        f'Analyzing {len(to_analyze_utterances)} of {len(utterances)} utterances..')

    coreresults, allmatches, corelevels, annotations = run_core_queries(
        to_analyze_utterances,
        queries_with_funcs,
        zc_embed,
        annotate)

    runs = AnalysisRun.objects.filter(transcript=transcript)
    if runs:  # An annotations file exists, base further results on this
        latest_run = runs.latest()
        reader = SAFReader(latest_run.annotation_file.path, method)
        coreresults = reader.document.to_allresults().coreresults
        annotations = reader.document.reformatted_annotations

    allresults = AllResults(transcript.name,
                            len(to_analyze_utterances),
                            coreresults,
                            None,
                            allmatches,
                            annotations)

    run_post_queries(allresults, queries_with_funcs)
    return allresults, queries_with_funcs


def run_core_queries(utterances: List[Utterance],
                     queries: List[QueryWithFunction],
                     zc_embed: bool,
                     annotate: bool):
    levels: Set[str] = set([])
    allmatches: SastaMatches = defaultdict(list)
    results: SastaResults = {}
    annotations = {}

    core_queries: List[QueryWithFunction] = [
        q for q in queries if q.query.process == core_process]

    for utt in utterances:
        if annotate:
            utt_res = utt_from_tree(utt.parse_tree, zc_embed)
        for q in core_queries:
            matches = single_query_single_utt(q.function, utt.syntree)

            if matches:
                if q.id in results:
                    results[q.id].update(
                        {utt.utt_id: len(matches)})
                else:
                    results[q.id] = Counter(
                        {utt.utt_id: len(matches)})
                for m in matches:
                    levels.add(q.query.level)
                    allmatches[(q.id, utt.utt_id)].append((m, utt.syntree))
                    if annotate:
                        begin = int(m.get('begin'))
                        hit = {
                            'level': q.query.level,
                            'item': q.query.item,
                            'fase': q.query.fase
                        }
                        utt_res[begin].hits.append(hit)

                if annotate:
                    annotations[utt.utt_id] = utt_res

    return (results, allmatches, levels, annotations or None)


def run_post_queries(allresults: SastaResults,
                     queries: List[QueryWithFunction]) -> None:
    post_queries: List[QueryWithFunction] = [
        q for q in queries if q.query.process == post_process]
    flat_queries: Dict[str, Query] = {q.id: q.query for q in queries}

    for q in post_queries:
        try:
            result = q.function(allresults, flat_queries)
            if result is not None:
                allresults.postresults[q.id] = result
        except Exception as e:
            # logger.warning(f'Failed to execute {q.function}')
            logger.exception(e)
