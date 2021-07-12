import os
import re
from collections import Counter
from io import BytesIO

import xlrd
import xlsxwriter
from sastadev import SD_DIR
from sastadev.counterfunctions import counter2liststr

ordA = ord('A')
comma = ','
xlsxext = '.xlsx'

idpat = r'^[TSA][0-9]{3}$'
idcpat = r'^[TSA][0-9]{3}c$'
idre = re.compile(idpat)
idcre = re.compile(idcpat)


def getshortloc(colctr, rowctr):
    # colctr must be smaller than 26
    colstr = chr((colctr % 26) + ordA)
    rowstr = str(rowctr + 1)
    result = colstr + rowstr
    return result


def readbaseform(infilename):
    basesheet = {}
    wb = xlrd.open_workbook(infilename)
    sheet = wb.sheet_by_index(0)
    startrow = 0
    startcol = 0
    lastrow = sheet.nrows
    lastcol = sheet.ncols
    for rowctr in range(startrow, lastrow):
        for colctr in range(startcol, lastcol):
            curval = sheet.cell_value(rowctr, colctr)
            if curval is not None and curval != '':
                basesheet[(rowctr, colctr)] = curval
    return basesheet


def is_id(word):
    result = idre.match(word)
    return result


def is_idc(word):
    result = idcre.match(word)
    return result


def idc2id(word):
    if word[-1] == 'c':
        result = word[:-1]
    else:
        result = word
    return result


def getval(allresults, idx):
    if idx in allresults.coreresults:
        result = allresults.coreresults[idx]
    elif idx in allresults.postresults:
        result = allresults.postresults[idx]
    else:
        result = ''
    return result


def val2str(aval):
    if isinstance(aval, Counter):
        result = counter2liststr(aval)
    elif isinstance(aval, list):
        result = comma.join(aval)
    else:
        result = str(aval)
    return result


def mktarspform(allresults, _, in_memory=False):
    global basesheet

    if not in_memory:
        (base, ext) = os.path.splitext(allresults.filename)
        target = base + '_TARSP-Form' + xlsxext
    else:
        target = BytesIO()

    workbook = xlsxwriter.Workbook(target, {"strings_to_numbers": True})
    worksheet = workbook.add_worksheet()

    for (rowctr, colctr) in basesheet:
        curval = str(basesheet[(rowctr, colctr)])
        if is_id(curval):
            newval = getval(allresults, curval)
            # write newval to the new sheet
            newvalstr = val2str(newval)
            worksheet.write(rowctr, colctr, newvalstr)
        elif is_idc(curval):
            urval = idc2id(curval)
            newval = getval(allresults, urval)
            cval = len(newval)
            newvalstr = val2str(cval)
            worksheet.write(rowctr, colctr, newvalstr)
        else:
            worksheet.write(rowctr, colctr, curval)

    # formatting
    textwrap = workbook.add_format()
    textwrap.set_text_wrap()
    boldbottom = workbook.add_format()
    boldbottom.set_bottom(5)
    textwrapcolumns = [2, 5, 8, 11, 14, 17, 20, 23]  # CFILORUX
    for col in textwrapcolumns:
        worksheet.set_column(col, col, None, textwrap)
    boldbottomrows = [12, 20, 28, 39, 44, 53, 56]
    for row in boldbottomrows:
        worksheet.set_row(row, row, boldbottom)

    columnwidths = {'B': 12, 'C': 14, 'D': 3, 'G': 3, 'H': 12, 'J': 3, 'K': 9, 'M': 3, 'N': 12, 'P': 3, 'S': 3, 'V': 3, 'W': 12, 'Y': 3, 'Z': 3}
    for row in columnwidths:
        range = row + ':' + row
        worksheet.set_column(range, columnwidths[row])

    # worksheet.set_landscape()
    worksheet.fit_to_pages(1, 1)
    worksheet.hide_gridlines(0)  # do not hide gridlines

    workbook.close()
    return target


# initialisation
basefilename = os.path.join(SD_DIR, 'form_templates', 'TARSP Form Current.xlsx')
basesheet = readbaseform(basefilename)
