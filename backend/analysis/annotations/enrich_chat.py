import itertools
from typing import List

from analysis.models import AssessmentMethod, Transcript
from analysis.results.results import AllResults
from chamd.chat_reader import ChatLine, ChatTier
from convert.chat_reader import ChatDocument


def find_doc_line(lines: List[ChatLine], uttno: int) -> ChatLine:
    # TODO: more efficient way to do this?
    return next((x for x in lines if x.uttid == uttno), None)


def enrich_chat(transcript: Transcript,
                allresults: AllResults,
                method: AssessmentMethod) -> ChatDocument:
    doc = ChatDocument.from_chatfile(transcript.content.path, transcript.corpus.method_category)

    # construct a mapping of uttno to uttid
    # because uttid is unknown to CHAT
    marked_utts = (x for x in transcript.utterances.all() if x.for_analysis)
    id_no_mapping = {
        u.utt_id: u.uttno for u in marked_utts
    }

    items = sorted(allresults.annotations.items())
    for utt_id, words in items:
        uttno = id_no_mapping.get(utt_id)
        doc_line = find_doc_line(doc.lines, uttno)
        flattened_hits = itertools.chain(*(w.hits for w in words))
        annotations = [x.get('item') for x in flattened_hits]
        if annotations:
            annotation_str = ', '.join(annotations)
            doc_line.tiers['xsyn'] = ChatTier(id='xsyn', text=annotation_str)
        # id_headers = [h for h in doc.headers if h.line.startswith('@ID')]
        # last_id_header = max(id_headers, key=attrgetter('linestartno'))
        # doc.headers.append(ChatHeader(
        #     line=f'@Comment:\tAnnotations on %xsyn-tiers generated by SASTA, using {method.category.name}',
        #     linestartno=last_id_header.linestartno+1))

    return doc