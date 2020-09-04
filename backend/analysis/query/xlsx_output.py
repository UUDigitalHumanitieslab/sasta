from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from analysis.query.functions import QueryWithFunction
from analysis.results.results import AllResults

from typing import List
from collections import Counter


def v1_to_xlsx(allresults: AllResults, queries: List[QueryWithFunction]):
    all_data = dict(allresults.coreresults, **allresults.postresults)

    wb = Workbook()
    worksheet = wb.active

    # header
    worksheet.append(['Query', 'Item', 'Fase', 'Utterance', 'Matches'])
    header = worksheet["1:1"]
    for cell in header:
        cell.font = Font(bold=True)

    query_mapping = {
        q.query.id: (q.query.fase or 0, q.query.item)
        for q in queries
        if q.query.id in all_data
    }
    sorted_queries = sorted(query_mapping.items(), key=lambda item: item[1][0])

    for qid, (fase, item) in sorted_queries:
        fase = fase if fase else 'nvt'
        data = all_data[qid]

        if isinstance(data, int):
            row = [qid, item, fase, 'total', data]
            worksheet.append(row)
        elif isinstance(data, Counter):
            first_row = [qid, item, fase, 'total', sum(data.values())]
            worksheet.append(first_row)
            for utt in sorted(data):
                row = [None, None, None, utt, data[utt]]
                worksheet.append(row)

    worksheet.auto_filter.ref = worksheet.dimensions
    return wb
