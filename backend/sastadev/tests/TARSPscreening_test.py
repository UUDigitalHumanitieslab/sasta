from sastadev.TARSPscreening import screening4stage
from sastadev.goldcountreader import get_goldcounts
import os


def test_tarspscreening():
    inpath = './goldcountstestin'
    testfilename = 'overzicht_Mieke.xlsx'
    testfullname = os.path.join(inpath, testfilename)
    testset = [(200, 'TARSP_MIEKE03_ID.xml'), (200, 'TARSP_MIEKE04_ID.xml'), (200, 'TARSP_MIEKE05_ID.xml'), (200, 'TARSP_MIEKE06_ID.xml'),
               (200, 'TARSP_MIEKE07_ID.xml'), (200, 'TARSP_MIEKE08_ID.xml')]
    for (uttcnt, tbn) in testset:
        print('Processing {}...'.format(tbn))
        tbndata = get_goldcounts(testfullname, tbn)
        thestage = screening4stage(uttcnt, tbndata)
        print('Stage of {}:  {}'.format(tbn, thestage))
