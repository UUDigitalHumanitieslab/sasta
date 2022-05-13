import traceback
from collections import Counter
from typing import List, Tuple

from analysis.models import AssessmentMethod
from analysis.query.functions import QueryWithFunction
from analysis.results.results import AllResults
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.styles.protection import Protection
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder

ROMAN_NUMS = [None, 'I', 'II', 'III',
              'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

BEFORE_WORDS_HEADERS = ['ID', 'Level', 'Unaligned']
AFTER_WORDS_HEADERS = ['Dummy', 'Fases', 'Commentaar']


def querycounts_to_xlsx(allresults: AllResults, queries: List[QueryWithFunction]):
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
    sorted_queries = sorted(
        sorted(
            query_mapping.items(),
            key=lambda item: item[0]
        ),
        key=lambda item: item[1][0]
    )

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
    autosize_columns(worksheet)

    return wb


def annotations_to_xlsx(allresults, method):
    try:
        wb = Workbook()
        worksheet = wb.active

        items = sorted(allresults.annotations.items())
        max_words = max([len(words) for (_, words) in items])
        headers = get_headers(max_words)
        worksheet.append(headers)

        zc_embeddings = method.category.zc_embeddings

        levels, lower_levels = get_levels(method)

        for utt_id, words in items:
            # Utt row, containing the word tokens
            words_row = [utt_id, 'Utt', None] + [w.word for w in words]

            # a cell for each word, and one to record phases
            level_rows = make_levels_rows(max_words, levels, utt_id)

            if zc_embeddings:
                zc_rows = make_zc_rows(max_words, utt_id, words)
            else:
                zc_rows = None

            comment_row = make_levels_rows(max_words, ['Commentaar'], utt_id)

            for i_word, word in enumerate(words):
                process_word(zc_embeddings, lower_levels, level_rows, zc_rows, i_word, word)

            append_utterance_rows(
                worksheet,
                words_row,
                level_rows,
                zc_rows,
                comment_row
            )

        format_worksheet(worksheet)
        autosize_columns(worksheet)

        return wb

    except Exception:
        traceback.print_exc()


def process_word(zc_embeddings, lower_levels, level_rows, zc_rows, i_word, word) -> None:
    '''Iterate over word hits and fill the corresponding level'''
    for hit in word.hits:
        if zc_embeddings and hit['level'].lower() == 'zc':
            i_level = word.zc_embedding
            process_hit(zc_rows, i_word, hit, i_level)
        else:
            i_level = lower_levels.index(hit['level'].lower())
            process_hit(level_rows, i_word, hit, i_level)


def process_hit(rows, i_word: int, hit, i_level: int) -> None:
    '''Add the hit to the right place in the rows, and append the fase as roman numeral'''
    rows[i_level][get_word_column(i_word)].add(hit['item'])
    try:
        rows[i_level][-1].append(
            ROMAN_NUMS[int(hit['fase'])])
    except Exception:
        pass


def get_word_column(word_index: int) -> int:
    return word_index + len(BEFORE_WORDS_HEADERS)


def append_utterance_rows(worksheet, words_row, levels_rows, zc_rows, comment_row) -> None:
    '''Append all rows for an utterance:
        words
        levels
        zc levels (optional)
    '''
    worksheet.append(words_row)
    append_level_rows(levels_rows, worksheet)
    append_level_rows(zc_rows, worksheet)
    worksheet.append(comment_row)


def append_level_rows(rows, worksheet) -> None:
    '''Condense cells to comma separated strings and append them to worksheet'''
    if not rows:
        return
    for row in rows:
        row = [','.join(sorted(cell)) or None
               if (isinstance(cell, set) or isinstance(cell, list))
               else cell
               for cell in row]
        worksheet.append(row)


def make_levels_rows(max_words: int, levels: List[str], utt_id: int):
    level_rows = [
        [utt_id, level]
        + [set([])]  # unaligned
        + [set([]) for _ in range(max_words + 1)]
        + [[]]  # fases
        # Everything after fases is undefined so fases are easy to find with -1
        for level in levels
    ]
    return level_rows


def make_zc_rows(max_words: int, utt_id: int, words):
    '''Rows for Zc levels. At least one, but more if deeper embeddings are present.
    '''
    embed_levels = {w.zc_embedding for w in words}
    max_embed = max(embed_levels)
    zc_levels = ['Zc'] * (max_embed + 1)  # N + 1 Zc levels
    return make_levels_rows(max_words, zc_levels, utt_id)


def get_headers(max_words: int) -> List[str]:
    word_headers = [f'Word{i}' for i in range(1, max_words + 1)]
    headers = BEFORE_WORDS_HEADERS + word_headers + AFTER_WORDS_HEADERS

    return headers


def get_levels(method: AssessmentMethod) -> Tuple[List[str], List[str]]:
    '''Lowercased list of all levels (excluding ZC)'''
    levels = method.category.levels
    if method.category.zc_embeddings:
        levels = [lv for lv in levels if lv.lower() != 'Zc'.lower()]
    lower_levels = list(map(str.lower, levels))
    return levels, lower_levels


def format_worksheet(worksheet) -> None:
    '''Locks all cells except annotation fields. Gives utterance rows a yellow background.'''

    # start by locking the entire sheet
    worksheet.protection.sheet = True
    unlocked = Protection(locked=False)

    header = worksheet["1:1"]
    for cell in header:
        # bold headers
        cell.font = Font(bold=True)

    # yelow background for each utterance row
    for row in list(worksheet.rows)[1:]:
        if row[1].value == 'Utt':
            for cell in row:
                cell.fill = PatternFill(
                    start_color="ffff00",
                    end_color="ffff00",
                    fill_type="solid")
        else:
            # unlock non-utterance rows
            # skip the first two columns (utt number and level)
            for cell in row[2:]:
                cell.protection = unlocked


def autosize_columns(worksheet) -> None:
    dim_holder = DimensionHolder(worksheet=worksheet)
    for col in range(worksheet.min_column, worksheet.max_column + 1):
        dim_holder[get_column_letter(col)] = ColumnDimension(
            worksheet, min=col, max=col, auto_size=True)
    worksheet.column_dimensions = dim_holder
