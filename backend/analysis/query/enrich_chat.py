from typing import List
from analysis.models import Transcript
from analysis.results.results import AllResults
from convert.chat_reader import ChatDocument
from chamd.chat_reader import ChatTier, ChatLine
import itertools


def find_doc_line(lines: List[ChatLine], uttid):
    # TODO: more efficient way to do this?
    return next((x for x in lines if x.uttid == uttid), None)


def enrich_chat(transcript: Transcript,
                allresults: AllResults) -> ChatDocument:
    doc = ChatDocument.from_chatfile(transcript.content.path)

    items = sorted(allresults.annotations.items())
    for utt_id, words in items:
        doc_line = find_doc_line(doc.lines, utt_id)
        flattened_hits = itertools.chain(*(w.hits for w in words))
        annotations = [x.get('item') for x in flattened_hits]
        if annotations:
            annotation_str = ', '.join(annotations)
            doc_line.tiers['xsyn'] = ChatTier(id='xsyn', text=annotation_str)

    return doc
