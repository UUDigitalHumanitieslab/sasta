from typing import Union

from lxml import etree as ET

from ..models import AssessmentMethod, AssessmentQuery, Transcript


def compile_xpath(query: str) -> Union[ET.XPath, None]:
    try:
        return ET.XPath('.'+query)
    except ET.XPathEvalError:
        return None
    except ET.XPathSyntaxError as e:
        print(e, query)
        return None


def query_transcript(transcript: Transcript, method: AssessmentMethod):
    queries = AssessmentQuery.objects.filter(method=method)
    nonempty_queries = queries.filter(query__isnull=False)

    query_funcs = [{'query_id': q.query_id, 'func': compile_xpath(q.query)}
                   for q in nonempty_queries if compile_xpath(q.query)]

    with open(transcript.parsed_content.path, 'rb') as f:
        with open('/Users/3248526/Documents/sasta_test_log.txt', 'w') as f_out:
            doc = ET.fromstring(f.read())
            utt_trees = doc.xpath('.//alpino_ds')

            for utt_tree in utt_trees:
                print(utt_tree.xpath('sentence')[
                      0].text.replace('\n', ''), file=f_out)
                for q_func in query_funcs:
                    res = q_func['func'](utt_tree)
                    if res:
                        print(q_func['query_id'], len(res), file=f_out)
