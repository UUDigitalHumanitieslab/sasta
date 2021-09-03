from .treebankfunctions import getattval

clausequery = './/node[@cat="smain" or @cat="ssub" or @cat="sv1" or @cat="whq" or @cat="whrel" or @cat="whsub" or @cat="cp" ]'
vrquery = './/node[@cat="whq" or @cat="whsub" or (@cat="whrel" and ../node[@cat="top"])]'


def empty(alist):
    return (alist == [])


def notempty(alist):
    return (not empty(alist))


def noposcatin(node):
    result = 'pt' not in node.attrib and 'pos' not in node.attrib and 'cat' not in node.attrib
    return result


def isindexnode(node):
    result = 'index' in node.attrib and noposcatin(node)
    return result


def isvcinforppart(node):
    rel = getattval(node, 'rel')
    cat = getattval(node, 'cat')
    if rel == 'vc' and cat in ['inf', 'teinf', 'ppart']:
        result = True
    else:
        result = False
    return result


def isrealnode(node):
    pt = getattval(node, 'pt')
    rel = getattval(node, 'rel')
    if pt == 'let':
        result = False
    elif isvcinforppart(node):
        result = False
    elif rel == 'svp' and pt in node.attrib:
        result = False
    elif isindexnode(node):
        result = False
    else:
        result = True
    return result


def isbodysv1(node):
    if node is None:
        result = False
    else:
        result = 'cat' in node.attrib and node.attrib['cat'] in ['sv1', 'ssub'] \
                 and 'rel' in node.attrib and node.attrib['rel'] == 'body'
    return result


def getnodecount(clause):
    nodectr = 0
    for child in clause:
        if isrealnode(child):
            nodectr += 1
        elif isbodysv1(child):
            nodectr += getnodecount(child)
        elif isvcinforppart(child):
            nodectr += getnodecount(child) - 1  # we do no count the verb because it is part of the 'gezegde'
    return nodectr


def sziplus(syntree, i):
    results = nodeiplus(syntree, i, clausequery)
    return results


def vr5plus(syntree):
    results = nodeiplus(syntree, 5, vrquery)
    return results


def nodeiplus(syntree, i, query):
    clauses = syntree.xpath(query)
    results = []
    for clause in clauses:
        nodecount = getnodecount(clause)
        if nodecount >= i:
            results.append(clause)
    return results


def sziplus6(syntree):
    results = sziplus(syntree, 6)
    return results
