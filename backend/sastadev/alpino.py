from sastadev import PARSE_FUNC, lexicon, treebankfunctions


def getalpinowordinfo(word):
    tree = PARSE_FUNC(word)
    relevantnode = treebankfunctions.find1(tree, '//node[parent::node[@cat="top"]]')
    if relevantnode is None:
        return []
    else:
        pos = treebankfunctions.getattval(relevantnode, 'pt')
        if pos == 'n':
            genus = treebankfunctions.getattval(relevantnode, 'genus')
            dehet = lexicon.het if genus == 'onz' else lexicon.de
            getal = treebankfunctions.getattval(relevantnode, 'getal')
            graad = treebankfunctions.getattval(relevantnode, 'graad')
            infl = 'd' if graad == 'dim' else ''
            infl += 'e' if getal == 'ev' else 'm'
            lemma = treebankfunctions.getattval(relevantnode, 'lemma')
            return([(pos, dehet, infl, lemma)])
        else:
            return []


def getdehetwordinfo(wrd):

    wordinfos = lexicon.getwordinfo(wrd)

    # we only want to consider nouns or words of unknown word class (such as kopje in CELEX)
    wordinfos = [wordinfo for wordinfo in wordinfos if wordinfo[0] in ['n', 'None']]
    # if any of the alternatives is a de-word, we empty the whole list
    if any([wordinfo[1] == lexicon.de for wordinfo in wordinfos]):
        wordinfos = []

    # if not found yet we check with Alpino
    if wordinfos != []:
        source = 'celex'
    else:
        wordinfos = getalpinowordinfo(wrd)
        source = 'alpino'
    return (wordinfos, source)
