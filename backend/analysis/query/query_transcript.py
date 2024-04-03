from collections import namedtuple
from typing import Tuple
from analysis.models import AssessmentMethod, Transcript
from sastadev.sastacore import SastaCoreParameters, sastacore
from sastadev.targets import get_targets
from lxml import etree
from sastadev.methods import Method


def prepare_parameters(infilename: str, method: Method, targets: int, annotate: bool) -> SastaCoreParameters:
    # TODO: check corr/corrn

    return SastaCoreParameters(
        annotationinput=annotate,
        themethod=method.to_sastadev(),
        infilename=infilename,
        targets=targets
    )


def prepare_treebanks(transcript: Transcript) -> Tuple[Tuple[str, etree.ElementTree]]:
    orig_fp = transcript.parsed_content.path
    corr_fp = transcript.corrected_content.path
    orig_treebank = etree.parse(orig_fp).getroot()
    corr_treebank = etree.parse(corr_fp).getroot()
    return (
        (orig_fp, orig_treebank),
        (corr_fp, corr_treebank)
    )


def run_sastacore(transcript: Transcript, method: AssessmentMethod, annotate: bool = False):
    orig_tb, corr_tb = prepare_treebanks(transcript)

    # Retrieve targets from corrected treebank
    targets = get_targets(corr_tb[1])
    params = prepare_parameters(corr_tb[0], method, targets, annotate)

    res = sastacore(
        origtreebank=orig_tb[1],
        correctedtreebank=corr_tb[1],
        annotatedfileresults=None,
        scp=params
    )

    return res
