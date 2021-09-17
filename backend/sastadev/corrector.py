''''
Jij moet er dan voor zorgen dat je in de CHAT file die je produceert iedere uiting afgaat en een call doet naar een functie

getcorrection
met als argument de string van de uiting.

Deze functie geeft dan terug een tuple (correction, metadata)

waarbij
•	correction een string is die je op moet nemen in de chat file als de verbeterde uiting
•	metadata metadata zijn a la PaQu (type, name, value) o.a. origutt van type text met als waarde de inputstring

'''

import copy
import re

from sastadev.alpino import getdehetwordinfo
from sastadev.cleanCHILDEStokens import cleantokens
from sastadev.dedup import (cleanwordofnort, findjaneenou, getfilledpauses,
                            getprefixwords, getrepeatedtokens)
from sastadev.deregularise import correctinflection
from sastadev.iedims import getjeforms
from sastadev.lexicon import de, dets, het, informlexicon, known_word
from sastadev.metadata import (bpl_node, bpl_none, bpl_word,
                               defaultbackplacement, defaultpenalty,
                               mkSASTAMeta)
from sastadev.namepartlexicon import isa_namepart
from sastadev.sastatok import sasta_tokenize
from sastadev.sastatoken import Token, tokenlist2stringlist
from sastadev.stringfunctions import (consonants, deduplicate, endsinschwa,
                                      fullworddehyphenate, monosyllabic,
                                      vowels)
from sastadev.sva import getsvacorrections
from sastadev.tokenmd import TokenListMD, TokenMD, mdlist2listmd
from sastadev.treebankfunctions import find1

SASTA = 'SASTA'

replacepattern = '{} [: {} ]'
metatemplate = '##META {} {} = {}'
slash = '/'
space = ' '

wrongdet_excluded_words = ['zijn', 'dicht', 'met']


def mkmeta(att, val, type='text'):
    result = metatemplate.format(type, att, val)
    return result


def anychars(chars):
    result = '[' + chars + ']'
    return result


def opt(pattern):
    result = '(' + pattern + ')?'
    return result


def replacement(inword, outword):
    result = replacepattern.format(inword, outword)
    return result


# duppattern = r'(.)\1{2,}'
# dupre = re.compile(duppattern)
gaatiepattern = r'^.*' + anychars(vowels) + opt(anychars(consonants)) + 'tie$'
gaatiere = re.compile(gaatiepattern)
neutersgnoun = 'boekje'  # seecet here an unambiguous neuter noun


basicreplacementlist = [('as', 'als'), ('isse', 'is'), ('ooke', 'ook'), ('innu', 'in de'), ('inne', 'in de'),
                        ('t', "'t"), ('dis', 'dit is'), ('das', 'dat is'), ('tis', 'dit is'), ('effjes', 'eventjes'),
                        ('effetjes', 'eventjes'), ('effe', 'even'), ('set', 'zet')]

basicreplacements = {}
# add @@metadata here; check some for alternatives
for w1, w2 in basicreplacementlist:
    basicreplacements[w1] = w2


def reduce(tokens):

    reducedtokens = tokens
    allmetadata = []

    allremovetokens = []
    allremovepositions = []
    filledpausetokens = getfilledpauses(reducedtokens)
    filledpausepositions = [token.pos for token in filledpausetokens]
    allremovetokens += filledpausetokens
    allremovepositions += filledpausepositions
    reducedtokens = [tok for tok in reducedtokens if tok not in filledpausetokens]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical', 'Filled Pause', 'Syntax') for token in filledpausetokens]
    allmetadata += metadata

    janeenoutokens = findjaneenou(reducedtokens)
    janeenoupositions = [token.pos for token in janeenoutokens]
    allremovetokens += janeenoutokens
    allremovepositions += janeenoupositions
    reducedtokens = [tok for tok in reducedtokens if tok not in janeenoutokens]
    metadata = [mkSASTAMeta(token, token, 'ExtraGrammatical', 'Filled Pause', 'Syntax') for token in janeenoutokens]
    allmetadata += metadata

    # short repetitions
    def cond(x, y):
        return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) < .5
    shortprefixtokens = getprefixwords(reducedtokens, cond)
    shortprefixpositions = [token.pos for token in shortprefixtokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, shortprefixtokens)
    allremovetokens += shortprefixtokens
    allremovepositions == shortprefixpositions
    metadata = [mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical', 'Short Repetition', 'Syntax') for token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in shortprefixtokens]

    # long repetitions
    def cond(x, y):
        return len(cleanwordofnort(x)) / len(cleanwordofnort(y)) >= .5
    longprefixtokens = getprefixwords(reducedtokens, cond)
    longprefixpositions = [token.pos for token in longprefixtokens]
    repeatedtokens = getrepeatedtokens(reducedtokens, longprefixtokens)
    allremovetokens += longprefixtokens
    allremovepositions == longprefixpositions
    metadata = [mkSASTAMeta(token, repeatedtokens[token], 'ExtraGrammatical', 'Long Repetition', 'Syntax') for token in reducedtokens if token in repeatedtokens]
    allmetadata += metadata
    reducedtokens = [tok for tok in reducedtokens if tok not in longprefixtokens]

    # @@add here the repeated word( sequence)s

    return (reducedtokens, allremovetokens, allmetadata)


def combinesorted(toklist1, toklist2):
    result = toklist1 + toklist2
    sortedresult = sorted(result, key=lambda tok: tok.pos)
    return sortedresult


def getcorrection(utt, tree=None, interactive=False):

    allmetadata = []
    rawtokens = sasta_tokenize(utt)
    wordlist = tokenlist2stringlist(rawtokens)

    tokens, metadata = cleantokens(rawtokens, repkeep=False)
    allmetadata += metadata
    tokensmd = TokenListMD(tokens, [])

    reducedtokens, allremovedtokens, metadata = reduce(tokens)
    reducedtokensmd = TokenListMD(reducedtokens, [])
    allmetadata += metadata

    alternativemds = getalternatives(reducedtokensmd, tree, 0)
    unreducedalternativesmd = [TokenListMD(combinesorted(alternativemd.tokens, allremovedtokens), alternativemd.metadata) for alternativemd in alternativemds]

    correctiontokensmd = unreducedalternativesmd[-1] if unreducedalternativesmd != [] else tokensmd

    correction = tokenlist2stringlist(correctiontokensmd.tokens)
    allmetadata += correctiontokensmd.metadata

    result = (correction, allmetadata)
    return result


def getcorrections(utt, method, tree=None, interactive=False):

    allmetadata = []
    rawtokens = sasta_tokenize(utt)
    wordlist = tokenlist2stringlist(rawtokens)

    tokens, metadata = cleantokens(rawtokens, repkeep=False)
    allmetadata += metadata
    tokensmd = TokenListMD(tokens, [])

    reducedtokens, allremovedtokens, metadata = reduce(tokens)
    reducedtokensmd = TokenListMD(reducedtokens, [])
    allmetadata += metadata

    alternativemds = getalternatives(reducedtokensmd, tree, 0)
    unreducedalternativesmd = [TokenListMD(combinesorted(alternativemd.tokens, allremovedtokens), alternativemd.metadata) for alternativemd in alternativemds]

    intermediateresults = unreducedalternativesmd if unreducedalternativesmd != [] else [tokensmd]

    results = []
    for ctmd in intermediateresults:
        correction = tokenlist2stringlist(ctmd.tokens)
        themetadata = allmetadata + ctmd.metadata
        results.append((correction, themetadata))
    return results


def getalternatives(origtokensmd, tree, uttid):

    tokensmd = explanationasreplacement(origtokensmd, tree)
    if tokensmd is None:
        tokensmd = origtokensmd

    tokens = tokensmd.tokens
    allmetadata = tokensmd.metadata
    newtokens = []
    alternatives = []
    alternativetokenmds = {}
    validalternativetokenmds = {}
    tokenctr = 0
    for token in tokens:
        tokenmd = TokenMD(token, allmetadata)
        alternativetokenmds[tokenctr] = getalternativetokenmds(tokenmd, tokens, tokenctr, tree, uttid)
        validalternativetokenmds[tokenctr] = getvalidalternativetokenmds(tokenmd, alternativetokenmds[tokenctr])
        tokenctr += 1

    # get all the new token sequences
    tokenctr = 0
    lvalidalternativetokenmds = len(validalternativetokenmds)
    altutts = [[]]
    newutts = []
    while tokenctr < lvalidalternativetokenmds:
        for tokenmd in validalternativetokenmds[tokenctr]:
            for utt in altutts:
                newutt = copy.copy(utt)
                newutt.append(tokenmd)
                newutts.append(newutt)
        altutts = newutts
        newutts = []
        tokenctr += 1

    # now turn each sequence of (token, md) pairs into a pair (tokenlist, mergedmetadata)
    newaltuttmds = []
    for altuttmd in altutts:
        newaltuttmd = mdlist2listmd(altuttmd)
        newaltuttmds.append(newaltuttmd)

    # combinations of tokens or their alternatives: de kopje, de stukkie, heeft gevalt

    allalternativemds = []
    for uttmd in newaltuttmds:
        uttalternativemds = getwrongdetalternatives(uttmd, tree, uttid)
        allalternativemds.append(uttalternativemds)

    allalternativemds2 = []
    for uttmd in allalternativemds:
        uttalternativemds = getsvacorrections(uttmd, tree, uttid)
        if uttalternativemds != []:
            allalternativemds2.append(uttalternativemds[0])
        else:
            allalternativemds2 = allalternativemds

    # final check whether the alternatives are improvements. It is not assumed that the original tokens is included in the alternatives
    finalalternativemds = lexcheck(tokensmd, allalternativemds2)

    return finalalternativemds


def lexcheck(intokensmd, allalternativemds):
    finalalternativemds = [intokensmd]
    for alternativemd in allalternativemds:
        diff_found = False
        include = True
        intokens = intokensmd.tokens
        outtokens = alternativemd.tokens
        for (intoken, outtoken) in zip(intokens, outtokens):
            if intoken != outtoken:
                diff_found = True
                if not known_word(outtoken.word):
                    include = False
                    break
        if diff_found and include:
            finalalternativemds.append(alternativemd)
    return finalalternativemds

# moved to metadata
# def mkSASTAMeta(token, nwt, name, value, cat, subcat=None, penalty=defaultpenalty, backplacement=defaultbackplacement):
#    result = Meta(name, value, annotatedposlist=[token.pos],
#                     annotatedwordlist=[token.word], annotationposlist=[nwt.pos],
#                     annotationwordlist=[nwt.word], cat=cat, subcat=subcat, source=SASTA, penalty=penalty,
#                     backplacement=backplacement)
#    return result


def updatenewtokenmds(newtokenmds, token, newwords, beginmetadata, name, value, cat, subcat=None,
                      penalty=defaultpenalty, backplacement=defaultbackplacement):
    for nw in newwords:
        nwt = Token(nw, token.pos)
        meta = mkSASTAMeta(token, nwt, name=name, value=value, cat=cat, subcat=subcat, penalty=penalty,
                           backplacement=backplacement)
        metadata = [meta] + beginmetadata
        newwordtokenmd = TokenMD(nwt, metadata)
        newtokenmds.append(newwordtokenmd)
    return newtokenmds


def gettokensplusxmeta(tree):
    '''
    converts the origutt into  list of xmeta elements
    :param tree: input tree
    :return: list of xmeta elements
    '''
    origutt = find1(tree, './/meta[@name="origutt"]/@value')
    tokens1 = sasta_tokenize(origutt)
    tokens2, metadata = cleantokens(tokens1, repkeep=False)
    return tokens2, metadata


def findxmetaatt(xmetalist, name, cond=lambda x: True):
    cands = [xm for xm in xmetalist if xm.name == name and cond(xm)]
    if cands == []:
        result = None
    else:
        result = cands[0]
    return result


def tokenreplace(oldtokens, newtoken):
    newtokens = []
    for token in oldtokens:
        if token.pos == newtoken.pos:
            newtokens.append(newtoken)
        else:
            newtokens.append(token)
    return newtokens


def explanationasreplacement(tokensmd, tree):
    # interpret single word explanation as replacement # this will work only after retokenistion of the origutt
    result = None
    origmetadata = tokensmd.metadata
    xtokens, xmetalist = gettokensplusxmeta(tree)
    explanations = [xm for xm in xmetalist if xm.name == 'Explanation']
    newtokens = copy.deepcopy(xtokens)
    newmetadata = origmetadata + xmetalist
    for explanation in explanations:
        newwordlist = explanation.annotationwordlist
        oldwordlist = explanation.annotatedwordlist
        tokenposlist = explanation.annotatedposlist
        if len(newwordlist) == 1 and len(tokenposlist) == 1 and len(oldwordlist) == 1:
            newword = newwordlist[0]
            oldwordpos = tokenposlist[0]
            oldword = oldwordlist[0]
            newtoken = Token(newword, oldwordpos)
            oldtoken = Token(oldword, oldwordpos)
            if known_word(newword):
                newtokens = tokenreplace(newtokens, newtoken)
                bpl = bpl_node if known_word(oldword) else bpl_word
                meta = mkSASTAMeta(oldtoken, newtoken, name='ExplanationasReplacement', value='ExplanationasReplacement',
                                   cat='Lexical Error', backplacement=bpl_node)
                newmetadata.append(meta)
                result = TokenListMD(newtokens, newmetadata)
    return result


def getalternativetokenmds(tokenmd, tokens, tokenctr, tree, uttid):
    token = tokenmd.token
    beginmetadata = tokenmd.metadata
    newtokenmds = []

    # decapitalize initial token  except when it is a known name
    if tokenctr == 0 and token.word.istitle() and not isa_namepart(token.word):
        newword = token.word.lower()

        newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                        name='Character Case', value='Lower case', cat='Orthography')

    # dehyphenate
    if not known_word(token.word):
        newwords = fullworddehyphenate(token.word, known_word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Dehyphenation', value='Dehyphenation', cat='Pronunciation',
                                        backplacement=bpl_word)

    # deduplicate jaaaaa -> ja; heeeeeel -> heel
    if not known_word(token.word):
        newwords = deduplicate(token.word, known_word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Emphasis', value='Phoneme lengthening', cat='Pronunciation',
                                        backplacement=bpl_word)

    # basic replacements replace as by als, isse by is
    if token.word in basicreplacements:
        newwords = [basicreplacements[token.word.lower()]]
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Informal pronunciation', value='Coda reduction', cat='Pronunciation',
                                        backplacement=bpl_none)

    # find document specific replacements

    # find organisation specific replacements

    # find childes replacements, preferably with vocabulary from the same age

    # gaatie
    if not known_word(token.word):
        newwords = gaatie(token.word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='Word combination', value='Cliticisation', cat='Pronunciation',
                                        backplacement=bpl_none)

    # extend to gaat-ie

    # dediacritisize

    # iedims
    if token.word.endswith('ie') or token.word.endswith('ies'):
        newwords = getjeforms(token.word)
        newtokenmds = updatenewtokenmds(newtokenmds, token, newwords, beginmetadata,
                                        name='RegionalForm', value='ieDim', cat='Morphology', backplacement=bpl_word)

    # overregularised verb forms: gevalt -> gevallen including  incl  wrong verb forms: gekeekt -> gekeken
    if not known_word(token.word):
        nwms = correctinflection(token.word)
        for nw, metavalue in nwms:
            newtokenmds += updatenewtokenmds(newtokenmds, token, [nw], beginmetadata,
                                             name='InflectionError', value=metavalue, cat='Morphology',
                                             backplacement=bpl_word)

    # wrong verb forms: gekeekt -> gekeken: done!

    # me ze (grote/oudere/ kleine) moeder /vader/zusje/ broer -> mijn

    # e-> e(n)
    if not known_word(token.word):
        if endsinschwa(token.word) and not monosyllabic(token.word):
            newword = token.word + 'n'
            if known_word(newword):
                newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                                name='Pronunciation Variant', value='N-drop after schwa',
                                                cat='Pronunciation', backplacement=bpl_word)

    # initial s -> z
    if not known_word(token.word):
        if token.word[0] == 's':
            newword = 'z' + token.word[1:]
            if known_word(newword):
                newtokenmds = updatenewtokenmds(newtokenmds, token, [newword], beginmetadata,
                                                name='Pronunciation Variant', value='Initial z devoicing',
                                                cat='Pronunciation', backplacement=bpl_word)

    # ...en -> e: groten  -> grote (if adjective); goten -> grote

    # drop e at the end incl duplicated consonants (ooke -> ook; isse -> is ? DOne, basicreplacements

    # losse e -> een / het / de

    for newtokenmd in newtokenmds:
        morenewtokenmds = getalternativetokenmds(newtokenmd, tokens, tokenctr, tree, uttid)
        newtokenmds += morenewtokenmds

    return newtokenmds


def getvalidalternativetokenmds(tokenmd, newtokenmds):

    validnewtokenmds = [tokenmd for tokenmd in newtokenmds if known_word(tokenmd.token.word)]
    if validnewtokenmds == []:
        validnewtokenmds = [tokenmd]
    return validnewtokenmds


def gaatie(word):
    results = []
    if gaatiere.match(word):
        if informlexicon(word[:-2]):  # and if it is a verb this is essential because now tie is also split into t ie
            result = space.join([word[:-2], word[-2:]])
            results.append(result)
    return results


def getwrongdetalternatives(tokensmd, tree, uttid):
    tokens = tokensmd.tokens
    metadata = tokensmd.metadata
    ltokens = len(tokens)
    tokenctr = 0
    newtokens = []
    while tokenctr < ltokens:
        token = tokens[tokenctr]
        if token.word in dets[de] and tokenctr < ltokens - 1:
            nexttoken = tokens[tokenctr + 1]
            # we want to exclude some words
            if nexttoken.word in wrongdet_excluded_words:
                wordinfos = []
            else:
                wordinfos, _ = getdehetwordinfo(nexttoken.word)
            if wordinfos != []:
                for wordinfo in wordinfos:  # if there are multiple alternatives we overwrite and therefore get the last alternative
                    (pos, dehet, infl, lemma) = wordinfo
                    if dehet == het and infl in ['e', 'de']:
                        # newcurtoken = replacement(token, swapdehet(token))
                        newcurtokenword = swapdehet(token.word)
                        newcurtoken = Token(newcurtokenword, token.pos)
                        meta = mkSASTAMeta(token, newcurtoken, name='GrammarError', value='deheterror', cat='Error',
                                           backplacement=bpl_node)
                        metadata.append(meta)
                    else:
                        newcurtokenword = token.word
                newtokens.append(Token(newcurtokenword, token.pos))
            else:
                newcurtokenword = token.word
                newtokens.append(token)
        else:
            newtokens.append(token)
        tokenctr += 1
    result = TokenListMD(newtokens, metadata)
    return result


def parseas(w, code):
    result = '[ @add_lex {} {} ]'.format(code, w)
    return result


def swapdehet(dedet):
    if dedet in dets[de]:
        deindex = dets[de].index(dedet)
    else:
        deindex = -1
    if dedet in dets[het]:
        hetindex = dets[het].index(dedet)
    else:
        hetindex = -1
    if deindex >= 0:
        result = dets[het][deindex]
    elif hetindex >= 0:
        result = dets[de][hetindex]
    else:
        result = None
    return result


def outputalternatives(tokens, alternatives, outfile):
    for el in alternatives:
        print(tokens[el], slash.join(alternatives[el]), file=outfile)


def mkchatutt(intokens, outtokens):
    result = []
    for (intoken, outtoken) in zip(intokens, outtokens):
        newtoken = intoken if intoken == outtoken else replacement(intoken, outtoken)
        result.append(newtoken)
    return result


def altmkchatutt(intokens, outtoken):
    result = []
    for intoken in intokens:
        newtoken = intoken if intoken == outtoken else replacement(intoken, outtoken)
        result.append(newtoken)
    return result
