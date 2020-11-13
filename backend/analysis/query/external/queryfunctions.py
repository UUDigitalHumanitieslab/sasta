from .treebankfunctions import (
    parent, is_left_sibling, getattval, get_left_siblings)


nietxpath = './/node[@lemma="niet"]'
wordxpath = './/node[@pt]'

vzn1xpath = './/node[ @cat="pp" and (node[@pt="vz"] and node[(@pt="n" or @pt="vnw") and @rel="obj1"] and not(node[@pt="vz" and @vztype="fin"]))]'
vzn2xpath = './/node[node[@lemma="in" and @rel="mwp"] and node[@lemma="deze" and @rel="mwp"]]'
vzn3xpath = './/node[@pt="vz" and ../node[(@lemma="dit" or @lemma="dat")  and @begin=../node[@pt="vz"]/@end and count(node)<=3] ]'


def xneg(stree):
    nodepairs = []
    nietnodes = stree.xpath(nietxpath)
    for nietnode in nietnodes:
        pnietnode = parent(nietnode)
        leftnietsiblings = get_left_siblings(nietnode)
        leftsiblings = get_left_siblings(pnietnode)
        ppnietnode = parent(pnietnode)
        if getattval(pnietnode, 'cat') == "advp" and len(leftsiblings) == 1 and getattval(ppnietnode, 'rel') == '--':
            result = True
            theleftsibling = leftsiblings[0]
        elif getattval(pnietnode, 'cat') != "advp" and getattval(pnietnode, 'rel') == '--' and len(leftnietsiblings) == 1:
            result = True
            theleftsibling = leftnietsiblings[0]
        else:
            result = False
        if result:
            nodepairs.append((theleftsibling, nietnode))
    if nodepairs == []:
        return None
    else:
        return nodepairs[0]


def xneg_neg(stree):
    (x, neg) = xneg(stree)
    return neg


def xneg_x(stree):
    (x, neg) = xneg(stree)
    return x


def VzN(stree):
    results = []
    results += stree.xpath(vzn1xpath)
    results += stree.xpath(vzn2xpath)
    results += stree.xpath(vzn3xpath)
    return results
