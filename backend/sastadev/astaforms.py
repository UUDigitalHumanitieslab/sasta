import os
from collections import Counter, defaultdict
from io import BytesIO

import xlsxwriter
from sastadev.treebankfunctions import getattval

green = '#00FF00'
red = '#FF0000'
orange = '#FFBB9A'
grey = '#B0B0B0'
# green = 'green'
# green = '#006100'
# red = '#9C0006'
# red = 'red'
# orange = '#9C6500'
# orange = 'yellow'


def getformfilename(infilename):
    (base, _) = os.path.splitext(infilename)
    formname = base + '_astaformulier' + '.xlsx'
    return formname


class ExcelForm:
    def __init__(self, tabel, scores):
        self.tabel = tabel
        self.scores = scores


class AstaFormData:
    def __init__(self, noundict, verbdict, vardict, uttlist):
        self.noundict = noundict
        self.verbdict = verbdict
        self.vardict = vardict
        self.uttlist = uttlist


formulatemplate1 = '=IF(B{}="Niet gevuld",B{},(B{}-Tabel!B{})/Tabel!C{})'


def applytemplate1(rowctr):
    result = formulatemplate1.format(rowctr, rowctr, rowctr, rowctr + 1, rowctr + 1)
    return result


formulatemplate2 = '=(B{}-Tabel!B{})/Tabel!C{}'


def applytemplate2(rowctr):
    result = formulatemplate2.format(rowctr, rowctr + 1, rowctr + 1)
    return result


formulatemplate3 = "=IF(ISERROR(ROUND('{}'!{}3,2)),\"Niet gevuld\",ROUND('{}'!{}3,2))"


def applytemplate3(sheet, colchar):
    result = formulatemplate3.format(sheet, colchar, sheet, colchar)
    return result


finietheidsindexscore = "=IF(ISERROR(ROUND(Uitingen!D3,2)),\"Niet gevuld\",ROUND(Uitingen!D3,2))"
pcuscore = "=IF(ISERROR(ROUND(Uitingen!B4/Uitingen!B1,2)),\"Niet gevuld\",ROUND(Uitingen!B4/Uitingen!B1,2))"

tabel = [['', 'GEM', 'SD'],
         ['Aantal zelfstandige naamwoorden', 48, 7.88],
         ['TTR zelfstandige naamwoorden', 0.76, 0.08],
         ['Lexicale werkwoorden', 29, 4.14],
         ['TTR lexical werkwoorden', 0.63, 0.11],
         ['Semantische parafasieën', 0, 0.57],
         ['Fonologische parafasieën', 0, 0.33],
         ['Neologismen', 0, 0],
         ['Aantal koppel/modaalwerkwoorden', 12, 4.15],
         ['MLU', 8.63, 1.74],
         ['Percentage correcte uitingen', 0.93, 0.06],
         ['Finietheidsindex', 0.99, 0.03],
         ['Aantal bijzinnen', 4.8, 2.78]]


scores = [['', 'Score', 'SD'],
          ['Aantal zelfstandige naamwoorden', "='ZNW & WW'!B1", "=(B2-Tabel!B3)/Tabel!C3"],
          ['TTR zelfstandige naamwoorden', applytemplate3('ZNW & WW', 'B'), applytemplate1(3)],
          ['Aantal lexicale werkwoorden', "='ZNW & WW'!F1", applytemplate2(4)],
          ['TTR lexicale werkwoorden', applytemplate3('ZNW & WW', 'F'), applytemplate1(5)],
          ['Semantische parafasieën', '', applytemplate2(6)],
          ['Fonologische parafasieën', '', applytemplate2(7)],
          ['Neologismen', '', '=IF(B8=0,"Normaal","Afwijkend")'],
          ['Aantal koppel/modaalwerkwoorden', '', applytemplate2(9)],
          ['MLU', applytemplate3('Uitingen', 'B'), applytemplate1(10)],
          ['Percentage correcte uitingen', pcuscore, applytemplate1(11)],
          ['Finietheidsindex', finietheidsindexscore, applytemplate1(12)],
          ['Aantal bijzinnen', '=Uitingen!F2', applytemplate2(13)]]

sheet2hiddenrows = [['Totaal', '=SUM(D6:D105)', '', '', '', '=SUM(H6:H105)'],
                    ['Aantal uniek', '=COUNTA(B6:B105)', '', '', '', '=COUNTA(F6:F105)'],
                    ['TTR', '=B2/B1', '', '', '', '=F2/F1'],
                    ['', '', '', '', '', '']
                    ]

sheet3hiddenrows = [['Aantal', '=COUNTA(B6:B105)', '', 'Som', 'Som', 'Som'],
                    ['Totaal', '=SUM(B6:B105)', '', '=SUM(D6:D105)', '=SUM(E6:E105)', '=SUM(F6:F105)'],
                    ['MLU', '=B2/B1', '', '=(D2/(D2+E2))', '', ''],
                    ['Correct', '=COUNTIF(C6:C105,"J")', '', '', '', '']
                    ]

sheet2header = ['Nummer', 'Zelfstandig naamwoord', 'Herhaling', 'Aantal', '', 'Lexicaal werkwoord', 'Herhaling', 'Aantal']
sheet2colwidths = [10, 25, 20, 10, 5, 25, 20, 10]
sheet3header = ['Uitingsnummer', 'Aantal woorden', 'Correct', "Goede PV's", "Foute en ontbrekende PV's", "Aantal bijzinnen", "Bijzonderheden"]


def writetable(tabel, ws, startrow=0, startcol=0, rhformat=None, chformat=None, cellformat=None):
    curcol = startcol
    currow = startrow
    for row in tabel:
        for el in row:
            if currow == startrow:
                theformat = rhformat
            elif curcol == startcol:
                theformat = chformat
            else:
                theformat = cellformat
            ws.write(currow, curcol, el, theformat)
            curcol += 1
        currow += 1
        curcol = startcol


def make_astaform(theform, astadata, target):
    workbook = xlsxwriter.Workbook(target, {"strings_to_numbers": True})
    bold = workbook.add_format({'bold': True})
    dd2 = workbook.add_format({'num_format': '0.00'})
    okformat = workbook.add_format({'bg_color': green})
    wrongformat = workbook.add_format({'bg_color': red})
    unfilledformat = workbook.add_format({'bg_color': orange})
    bggrey = workbook.add_format({'bg_color': grey})

    condformat1a = {'type': 'cell', 'criteria': 'between', 'minimum': -2, 'maximum': 2, 'format': okformat}
    condformat1b = {'type': 'cell', 'criteria': 'not between', 'minimum': -2, 'maximum': 2, 'format': wrongformat}
    condformat1c = {'type': 'cell', 'criteria': 'equal to', 'value': '"Niet gevuld"', 'format': unfilledformat}
    condformat2a = {'type': 'formula', 'criteria': '=$B$8<>0', 'format': wrongformat}
    condformat2b = {'type': 'formula', 'criteria': '=$B$8=0', 'format': okformat}
    condformat2c = {'type': 'cell', 'criteria': 'equal to', 'value': '"Niet gevuld"', 'format': unfilledformat}

    worksheet1 = workbook.add_worksheet('Uitkomstentabel')
    worksheet2 = workbook.add_worksheet('ZNW & WW')
    worksheet3 = workbook.add_worksheet('Uitingen')
    worksheet4 = workbook.add_worksheet('Tabel')

    # worksheet1
    worksheet1.set_column(0, 0, 30)
    worksheet1.set_column(1, 2, 12)
    worksheet1.hide_gridlines(option=2)
    worksheet1.conditional_format('$C$2:$C$7', condformat1a)
    worksheet1.conditional_format('$C$2:$C$7', condformat1b)
    worksheet1.conditional_format('$C$2:$C$7', condformat1c)
    worksheet1.conditional_format('$C$9', condformat1a)
    worksheet1.conditional_format('$C$9', condformat1b)
    worksheet1.conditional_format('$C$9', condformat1c)
    worksheet1.conditional_format('$C$10:$C$13', condformat1a)
    worksheet1.conditional_format('$C$10:$C$13', condformat1b)
    worksheet1.conditional_format('$C$10:$C$13', condformat1c)
    worksheet1.conditional_format('$C$8', condformat2a)
    worksheet1.conditional_format('$C$8', condformat2b)
    worksheet1.conditional_format('$C$8', condformat2c)

    writetable(theform.scores, worksheet1, rhformat=bold, chformat=bold, cellformat=dd2)
    worksheet1.write('$B$6', '', bggrey)
    worksheet1.write('$B$7', '', bggrey)
    worksheet1.write('$B$8', '', bggrey)
    worksheet1.write('$B$9', '', bggrey)

    for (loc, count) in astadata.vardict.items():
        worksheet1.write(loc, count)

    # worksheet2
    writetable(sheet2hiddenrows, worksheet2)

    colctr = 0
    for (el, w) in zip(sheet2header, sheet2colwidths):
        worksheet2.write(4, colctr, el, bold)
        worksheet2.set_column(colctr, colctr, w)
        colctr += 1

    rowctr = 5
    for i in range(100):
        worksheet2.write(rowctr, 0, i + 1)
        rowctr += 1

    rowctr = 5
    wcol = 1
    freqcol = 3
    for (w, cnt) in astadata.noundict.items():
        worksheet2.write(rowctr, wcol, w)
        worksheet2.write(rowctr, freqcol, cnt)
        rowctr += 1

    rowctr = 5
    wcol = 5
    freqcol = 7
    for (w, cnt) in astadata.verbdict.items():
        worksheet2.write(rowctr, wcol, w)
        worksheet2.write(rowctr, freqcol, cnt)
        rowctr += 1

    for rowctr in range(4):
        worksheet2.set_row(rowctr, None, None, {'hidden': True})

    # workasheet3
    writetable(sheet3hiddenrows, worksheet3)

    colctr = 0
    for el in sheet3header:
        worksheet3.write(4, colctr, el, bold)
        colctr += 1
    worksheet3.set_column(0, colctr, 20)

    rowctr = 5
    writetable(astadata.uttlist, worksheet3, startrow=rowctr)

    for rowctr in range(4):
        worksheet3.set_row(rowctr, None, None, {'hidden': True})

    # worksheet4
    worksheet4.set_column(0, 0, 30)

    writetable(theform.tabel, worksheet4, startrow=1, rhformat=bold)

    return workbook, target


def sumctr(ctr):
    result = sum(ctr.values())
    return result


def getvardict(allresults):
    sempar = 'B6'
    phonpar = 'B7'
    neo = 'B8'
    KM = 'B9'
    semparcount = sumctr(allresults.coreresults['A026']) if 'A026' in allresults.coreresults else 0
    phonparcount = sumctr(allresults.coreresults['A008']) if 'A008' in allresults.coreresults else 0
    neocount = sumctr(allresults.coreresults['A022']) if 'A022' in allresults.coreresults else 0
    Kcount = sumctr(allresults.coreresults['A013']) if 'A013' in allresults.coreresults else 0
    Mcount = sumctr(allresults.coreresults['A020']) if 'A020' in allresults.coreresults else 0
    KMcount = Kcount + Mcount
    result = {sempar: semparcount, phonpar: phonparcount, neo: neocount, KM: KMcount}
    return result


def update(resultdict, ctrdict, key, prop):
    if key in ctrdict:
        ctr = ctrdict[key]
        for uttid in ctr:
            resultdict[uttid][prop] = ctr[uttid]


def updatewithctr(resultdict, ctr, prop):
    for uttid in ctr:
        resultdict[uttid][prop] = ctr[uttid]


def dictget(dct, keyname):
    if keyname in dct:
        result = dct[keyname]
    else:
        result = ''
    return result


def resultdict2table(resultdict):
    table = []
    for uttid in resultdict:
        uttid_dict = resultdict[uttid]
        wc = dictget(uttid_dict, 'wc')
        correct = dictget(uttid_dict, 'correct')
        if correct != '':
            correct = 'J'
        okpvs = dictget(uttid_dict, 'okpvs')
        foutepvs = dictget(uttid_dict, 'foutepvs')
        bijzincount = dictget(uttid_dict, 'bijzincount')
        remarks = dictget(uttid_dict, 'remarks')
        paddeduttid = str(uttid).rjust(3, '0')
        newrow = [paddeduttid, wc, correct, okpvs, foutepvs, bijzincount, remarks]
        table.append(newrow)
    sortedtable = sorted(table, key=lambda row: row[0])
    return sortedtable


def getuttlist(allresults):
    resultdict = defaultdict(lambda: defaultdict(int))
    update(resultdict, allresults.postresults, 'A047', 'wc')
    update(resultdict, allresults.coreresults, 'A004', 'correct')
    update(resultdict, allresults.coreresults, 'A024', 'okpvs')
    subpvs = allresults.coreresults['A032'] if 'A032' in allresults.coreresults else Counter()
    delpvs = allresults.coreresults['A033'] if 'A033' in allresults.coreresults else Counter()
    tijdfoutpvs = allresults.coreresults['A041'] if 'A041' in allresults.coreresults else Counter()
    foutepvs = subpvs + delpvs + tijdfoutpvs
    updatewithctr(resultdict, foutepvs, 'foutepvs')
    update(resultdict, allresults.coreresults, 'A003', 'bijzincount')

    result = resultdict2table(resultdict)
    return result


def astaform(allresults, _, in_memory=False):
    noundict = defaultdict(int)
    verbdict = defaultdict(int)
    allmatches = allresults.allmatches
    for el in allmatches:
        (qid, uttid) = el
        if qid == 'A021':
            for amatch in allmatches[el]:
                # theword = normalizedword(amatch[0])
                theword = getattval(amatch[0], 'lemma')
                noundict[theword] += 1
        if qid == 'A018':
            for amatch in allmatches[el]:
                # theword = normalizedword(amatch[0])
                theword = getattval(amatch[0], 'lemma')
                verbdict[theword] += 1
    vardict = getvardict(allresults)
    uttlist = getuttlist(allresults)
    astadata = AstaFormData(noundict, verbdict, vardict, uttlist)
    theform = ExcelForm(tabel, scores)

    if in_memory:
        target = BytesIO()
    else:
        target = getformfilename(allresults.filename)

    theworkbook, target = make_astaform(theform, astadata, target)
    theworkbook.close()
    return target
