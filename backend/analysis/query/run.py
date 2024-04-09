import logging
from collections import Counter, defaultdict
from typing import Dict, List, Set
from analysis.annotations.safreader import SAFReader
from analysis.models import (AnalysisRun, AssessmentMethod, AssessmentQuery,
                             Transcript, Utterance)
from analysis.query.query_transcript import run_sastacore
from analysis.results.results import SastaMatches, SastaResults

from sastadev.query import Query, core_process, post_process, pre_process
from sastadev.allresults import AllResults

from .functions import (QueryWithFunction, compile_queries, filter_queries,
                        single_query_single_utt, utt_from_tree)

logger = logging.getLogger('sasta')


def annotate_transcript(transcript: Transcript, method: AssessmentMethod) -> AllResults:
    allresults, _samplesize = run_sastacore(transcript, method)
    return allresults


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
    utterance_syntrees = [(x.utt_id, x.syntree) for x in to_analyze_utterances]
    allutts = {utt.utt_id: utt.word_list for utt in to_analyze_utterances}
    logger.info(
        f'Analyzing {len(to_analyze_utterances)} of {len(utterances)} utterances..')

    coreresults, allmatches, exact_results, corelevels, annotations = run_core_queries(
        to_analyze_utterances,
        queries_with_funcs,
        zc_embed,
        annotate)

    annotationinput = False
    runs = AnalysisRun.objects.filter(transcript=transcript)
    if runs:  # An annotations file exists, base further results on this
        latest_run = runs.latest()
        reader = SAFReader(filepath=latest_run.annotation_file.path,
                           method=method, transcript=transcript)
        coreresults = reader.document.to_allresults().coreresults
        annotations = reader.document.reformatted_annotations
        exact_results = reader.document.exactresults
        annotationinput = True

    allresults = AllResults(filename=transcript.name,
                            uttcount=len(to_analyze_utterances),
                            coreresults=coreresults,
                            exactresults=exact_results,
                            postresults=None,
                            allmatches=allmatches,
                            annotations=annotations,
                            analysedtrees=utterance_syntrees,
                            annotationinput=annotationinput,
                            allutts=allutts
                            )

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
    exact_results = defaultdict(list)

    core_queries: List[QueryWithFunction] = sorted(
        [q for q in queries if q.query.process in [pre_process, core_process]],
        key=lambda x: (x.query.process, x.query.id))

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
                    # Record the match including the syntree
                    allmatches[(q.id, utt.utt_id)].append((m, utt.syntree))
                    # Record the exact word where the query was matched

                    word_index = next((i for i, item in enumerate(
                        utt.word_position_mapping) if item["begin"] == int(m.get('begin'))), None)
                    # exact_results[q.id].append((utt.utt_id, int(m.get('begin')) + 1))
                    exact_results[q.id].append((utt.utt_id, word_index))

                    if annotate:
                        begin = int(m.get('begin'))
                        hit = {
                            'level': q.query.level,
                            'item': q.query.item,
                            'fase': q.query.fase
                        }
                        matched_word = next(
                            (w for w in utt_res if w.begin == begin), None)
                        if matched_word:
                            matched_word.hits.append(hit)
                        else:
                            logger.warning(
                                f'Found hit ({q.query.level}, {q.query.item}, {q.query.fase}) for non-exising begin attr "{begin}"')
                if annotate:
                    annotations[utt.utt_id] = utt_res

    return (results, allmatches, exact_results, levels, annotations or None)


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
