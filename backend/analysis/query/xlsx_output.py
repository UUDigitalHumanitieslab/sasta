import traceback
from collections import Counter
from typing import List

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter

from analysis.query.functions import QueryWithFunction
from analysis.results.results import AllResults

LEVELS = ['Sz', 'Zc', 'Wg', 'VVW']
ROMAN_NUMS = [None, 'I', 'II', 'III',
              'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']


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

    # column widths
    worksheet = autosize_columns(worksheet)

    return wb


def v2_to_xlsx(allresults, method, zc_embeddings=False):
    try:
        wb = Workbook()
        worksheet = wb.active

        # items = sorted(data['results'].items())
        items = allresults.annotations.items()
        items = sorted(items)
        max_words = max([len(words) for (_, words) in items])
        word_headers = [f'Word{i}' for i in range(1, max_words + 1)]
        headers = ['ID', 'Level'] + word_headers + \
            ['Dummy', 'Unaligned', 'Fases', 'Commentaar']
        worksheet.append(headers)
        # levels = sorted(list(data['levels']))
        # levels = LEVELS
        levels = method.category.levels

        # How many ZC levels are there?
        if zc_embeddings:
            levels = [lv for lv in levels if lv != 'Zc']
            max_embed = 0
            for _, words in items:
                embed_levels = {
                    w.zc_embedding for w in words if w.zc_embedding}
                if embed_levels:
                    max_embed = max(max_embed, max(embed_levels))
            embed_range = range(0, max_embed + 1)

        lower_levels = [l.lower() for l in levels]
        for utt_id, words in items:
            # Utt row, containing the word tokens
            words_row = [utt_id, 'Utt'] + [w.word for w in words]

            # trailing empty cells, necesarry?
            words_row += [None]*(len(headers) - len(words_row))

            # a cell for each word, and one to record phases
            level_rows = [[utt_id, level]
                          + [set([]) for _ in range(max_words + 1)]
                          + [None]
                          + [[]]
                          for level in levels]

            if zc_embeddings:
                zc_rows = [[utt_id, 'Zc']
                           + [set([]) for _ in range(max_words + 1)]
                           + [None]
                           + [[]]
                           for _ in embed_range]

            # iterate over hits
            # fill in items on their respective level
            # leaving cells without hits as None
            for i_word, word in enumerate(words):
                for hit in word.hits:
                    if zc_embeddings and hit['level'].lower() == 'zc':
                        i_level = word.zc_embedding
                        # print(word.zc_embedding)
                        zc_rows[i_level][i_word + 2].add(hit['item'])
                        try:
                            zc_rows[i_level][-1].append(
                                ROMAN_NUMS[int(hit['fase'])])
                        except Exception:
                            pass
                    else:
                        i_level = lower_levels.index(hit['level'].lower())
                        print(*level_rows, sep='\n')
                        # print(level_rows[i_level])
                        print(i_level)
                        print(i_word+2)
                        level_rows[i_level][i_word + 2].add(hit['item'])

                        try:
                            level_rows[i_level][-1].append(
                                ROMAN_NUMS[int(hit['fase'])])
                        except Exception:
                            pass

            worksheet.append(words_row)
            # condense cells and append to xlsx
            for row in level_rows:
                row = [','.join(sorted(cell)) or None
                       if (isinstance(cell, set) or isinstance(cell, list))
                       else cell
                       for cell in row]
                worksheet.append(row)
            if zc_embeddings:
                for row in zc_rows:
                    row = [','.join(sorted(cell)) or None
                           if (isinstance(cell, set) or isinstance(cell, list))
                           else cell
                           for cell in row]
                    worksheet.append(row)

        # Formatting
        header = worksheet["1:1"]
        for cell in header:
            # bold headers
            cell.font = Font(bold=True)

        nth_row = len(levels) + 1 + \
            len(embed_range) if zc_embeddings else len(levels) + 1
        for i, row in enumerate(worksheet.rows):
            # yellow background for each utterance row
            if i % nth_row == 1:
                for cell in row:
                    cell.fill = PatternFill(
                        start_color="ffff00",
                        end_color="ffff00",
                        fill_type="solid")

        # column widths
        worksheet = autosize_columns(worksheet)

        return wb

    except Exception:
        traceback.print_exc()


def autosize_columns(worksheet):
    dim_holder = DimensionHolder(worksheet=worksheet)
    for col in range(worksheet.min_column, worksheet.max_column + 1):
        dim_holder[get_column_letter(col)] = ColumnDimension(
            worksheet, min=col, max=col, auto_size=True)
    worksheet.column_dimensions = dim_holder
    return worksheet
