from typing import List
from pprint import pprint

from lxml import etree as ET

from ..models import AssessmentMethod, AssessmentQuery, Transcript, Utterance


def query_transcript(transcript: Transcript, method: AssessmentMethod):
    queries = AssessmentQuery.objects.filter(method=method)
    xpath_queries = queries.filter(query__isnull=False)

    results = []

    with open(transcript.parsed_content.path, 'rb') as f:
        content = f.read()
        for q in xpath_queries:
            matches = single_query(q, ET.fromstring(content))
            if matches:
                print(q.query_id)
                print(q.query)
                for m in matches:
                    print(m.text)
                    print(m.tag)
                    print(m)
                    print('--')
                print('========')
    #             results.append({'query_id': q.query_id, 'matches': [
    #                            (m.text, m) for m in matches]})
    # with open('/Users/3248526/Documents/sasta_test_log.txt', 'w') as f_out:
    #     pprint(results, f_out)


def single_query(query_object: AssessmentQuery, doc):
    matches = doc.xpath(query_object.query)
    return matches
