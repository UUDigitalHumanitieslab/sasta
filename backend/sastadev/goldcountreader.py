import os
import xlrd
from sastadev import SDLOGGER

gcadd = '_count_tsv'
txtext = ".txt"
tab = '\t'
IDheaders = ['id']
uttcountheaders = ['uttcount', 'uttcounts']


def oldget_goldcounts(infilename, treebankname):
    '''
    Reads the file with name infilename in SASTA GoldCount Format (SGCF)
    Excel file with one column with header ID,
    :param infilename:
    :param treebankname: the name of the file containing the treebank
    :return: a dictionary  with as  key a tuple (level, item) and as value a Counter  with key uttid and value its count
    '''

    (_, tail) = os.path.split(treebankname)
    (cleantreebankname, ext) = os.path.splitext(tail)

    thedata = {}

    # To open Workbook
    wb = xlrd.open_workbook(infilename)
    sheet = wb.sheet_by_index(0)

    startrow = 0
    startcol = 0
    headerrow = 0
    lastrow = sheet.nrows
    lastcol = sheet.ncols
    idcol = None
    treebankcol = None

    for rowctr in range(startrow, lastrow):
        if rowctr == headerrow:
            for colctr in range(startcol, lastcol):
                curcell = sheet.cell_value(rowctr, colctr)
                lccurcell = curcell.lower().strip()
                if lccurcell in IDheaders:
                    idcol = colctr
                elif curcell == cleantreebankname:
                    treebankcol = colctr
        else:
            if idcol is None:
                SDLOGGER.error('no ID column found')
                exit(-1)
            if treebankcol is None:
                SDLOGGER.error('No column found for Treebank {}.'.format(treebankname))
                exit(-1)
            theid = sheet.cell_value(rowctr, idcol)
            thecount = sheet.cell_value(rowctr, treebankcol)
            if thecount != '':
                # make it robust here against nonnumber strings
                thecountint = int(thecount)
                thedata[theid] = thecountint

    return thedata


def get_goldcounts(infilename):
    '''
    Reads the file with name infilename in SASTA GoldCount Format (SGCF)
    Excel file with one column with header ID, and one header uttcount. All other columns are ignored
    :param infilename:
    :return: a dictionary  with as  key a tuple (level, item) and as value a Counter  with key uttid and value its count
    '''

    thedata = {}

    # To open Workbook
    wb = xlrd.open_workbook(infilename)
    sheet = wb.sheet_by_index(0)

    startrow = 0
    startcol = 0
    headerrow = 0
    lastrow = sheet.nrows
    lastcol = sheet.ncols
    idcol = None
    uttcountcol = None

    for rowctr in range(startrow, lastrow):
        if rowctr == headerrow:
            for colctr in range(startcol, lastcol):
                curcell = sheet.cell_value(rowctr, colctr)
                lccurcell = curcell.lower().strip()
                if lccurcell in IDheaders:
                    idcol = colctr
                elif lccurcell in uttcountheaders:
                    uttcountcol = colctr
        else:
            if idcol is None:
                SDLOGGER.error('no ID column found')
                break
            elif uttcountcol is None:
                SDLOGGER.error('No uttcount column found')
                break
            else:
                theid = sheet.cell_value(rowctr, idcol)
                thecount = sheet.cell_value(rowctr, uttcountcol)
                if thecount != '':
                    # make it robust here against nonnumber strings
                    thecountint = int(thecount)
                    thedata[theid] = thecountint

    return thedata
