'''
TARSP Screening Procedre (determining the stage of grammatical development)
Based on Schlichting 2015 Chapter Screening (p. 94- 96)

Parameters:
    stage1threshold: implements 'exclusively or almost exclusively one word sentences, set to 95%
    uttcountthreshold: minimum # utterances in the sample, set to 200 based on Schlichting 2005:94


function to expose to other modules is: screening4stage(uttcount, results)

'''
from sastadev.allresults import scores2counts
from sastadev import SDLOGGER

stage1threshold = 95
uttcountthreshold = 200

OndB = 'T064'
VCW = 'T099'
OndVC = 'T071'
OndW = 'T072'
BW = 'T028'
OndWVC = 'T076'
ik = 'T047'
HwwZ = 'T046'
VCWG = 'T101'
WWWG = 'T127'
BWWG = 'T019'
OndWG = 'T070'
OndWBVC = 'T075'
VzBepZn = 'T116'
en = 'T036'
het = 'T041'
VCWOndBB = 'T100'
OndWVCVCoptX = 'T077'
Nevenschikkende = 'T061'
VCbijzin = 'T098'
S6plus = 'T003'
BBijzin = 'T011'
Verbnieten = ''  # @@
wij = 'T128'
Wond5 = 'T131'
Vr5plus = 'T113'
hetZn = 'T042'
ditdatZn = 'T034'
Verbnietenalsmaar = ''  # @@
verltijd = 'T105'
Zn = 'T145'
BvB = 'T023'
W = 'T119'


def OK(queryid, results):
    result = queryid in results and results[queryid] > 0
    return result


def qcount(queryid, results):
    if queryid in results:
        result = results[queryid]
    else:
        result = 0
    return result


def stage2(results):
    cond1 = OK(OndB, results) or OK(OndVC, results)
    cond2 = OK(VCW, results) or OK(OndW, results) or OK(BW, results)
    result = cond1 and cond2
    return result


def stage3(results):
    WGOK = OK(VCWG, results) or OK(WWWG, results) or OK(BWWG, results) or OK(OndWG, results)
    OndWVCOK = OK(OndWVC, results)
    ikOK = OK(ik, results)
    HwwZOK = OK(HwwZ, results)
    baselist = [OndWVCOK, ikOK, HwwZOK, WGOK]
    resultlist = [b for b in baselist if b]
    result = len(resultlist) >= 3
    return result


def stage4(results):
    OndWBVCOK = OK(OndWBVC, results)
    VzBepZnOK = OK(VzBepZn, results)
    enOK = OK(en, results)
    hetOK = OK(het, results)
    baselist = [OndWBVCOK, VzBepZnOK, enOK, hetOK]
    resultlist = [b for b in baselist if b]
    result = len(resultlist) >= 3
    return result


def stage5(results):
    VCWOndBBOK = OK(VCWOndBB, results)
    OndWVCVCoptXOK = OK(OndWVCVCoptX, results)
    NevenschikkendeOK = OK(Nevenschikkende, results)
    VCbijzinOK = OK(VCbijzin, results)
    S6plusOK = OK(S6plus, results)
    BBijzinOK = OK(BBijzin, results)
    VerbnietenOK = OK(Verbnieten, results)
    wijOK = OK(wij, results)
    cond1 = VCWOndBBOK or OndWVCVCoptXOK
    cond2 = NevenschikkendeOK or VCbijzinOK or S6plusOK or BBijzinOK
    baselist = [cond1, cond2, VerbnietenOK, wijOK]
    resultlist = [b for b in baselist if b]
    result = len(resultlist) >= 3
    return result


def stage6(results):
    Wond5OK = OK(Wond5, results)
    Vr5plusOK = OK(Vr5plus, results)
    hetZnOK = OK(hetZn, results)
    ditdatZnOK = OK(ditdatZn, results)
    VerbnietenalsmaarOK = OK(Verbnietenalsmaar, results)
    verltijdOK = OK(verltijd, results)
    cond1 = Wond5OK or Vr5plusOK
    cond2 = hetZnOK or ditdatZnOK
    baselist = [cond1, cond2, VerbnietenalsmaarOK, verltijdOK]
    resultlist = [b for b in baselist if b]
    result = len(resultlist) >= 3
    return result


def stage1(results):
    BvBqcount = qcount(BvB, results)
    Wqcount = qcount(W, results)
    Znqcount = qcount(Zn, results)
    stage1count = BvBqcount + Wqcount + Znqcount
    allresults = [results[qid] for qid in results]
    sumallresults = sum(allresults)
    if sumallresults != 0:
        proportion = stage1count / sumallresults * 100
    else:
        proportion = 0
        SDLOGGER.warning('No results found. Output unreliable')
    result = proportion >= stage1threshold
    return result


def screening(results):
    stages = {}
    stages[6] = stage6(results)
    stages[5] = stage5(results)
    stages[4] = stage4(results)
    stages[3] = stage3(results)
    stages[2] = stage2(results)
    stages[1] = stage1(results) and not stages[2]
    result = None
    for s in range(6, 0, -1):
        # stageslogger.info('Checking stage %s', s)
        if result is None and stages[s]:
            result = s
            # for ls in range(s,0,-1):
            #    if not stages[ls]:
            #        print('Warning. Stage is {} but lower stage {} conditions are not met'. format(s,ls), file=sys.stderr)
    return result


def tarsp_screening(allresults, _):
    resultscounts = scores2counts(allresults.coreresults)
    result = screening4stage(allresults.uttcount, resultscounts)
    return result


def screening4stage(uttcount, results):
    '''
    determines the stage of grammaticl development based on two inputs:
    :param uttcount: size of the sample in # utterances. Values lower than 200 lead to unreliable results
    :param results: dictionary containing (queryid, count) pairs obtained for the sample by sasta doqueries
    :return:
    '''
    #   ;param thefilename: name of the treebank file
    #    (inbase, ext) = os.path.splitext(thefilename)
    #    stagesexplainfile = inbase + 'stage_explanation' + '.txt'
    #    stageslogger = logging.getLogger('Stages:')
    #    stageslogger.setLevel(logging.INFO)
    #    ch = logging.FileHandler(stagesexplainfile)
    #    ch.setLevel(logging.INFO)
#    stageslogger.addHandler(ch)

    if uttcount < uttcountthreshold:
        message = 'TARSP Screening: Less than {} utterances ({}). Results not reliable'.format(uttcountthreshold, uttcount)
        SDLOGGER.warning(message)
        # print(message)
    result = screening(results)
    return result
