from sastadev.treebankfunctions import parent, getattval, get_left_siblings
from sastadev.macros import expandmacros


nietxpath = './/node[@lemma="niet"]'
wordxpath = './/node[@pt]'

vzn1basexpath = './/node[ @cat="pp" and (node[@pt="vz"] and node[(@pt="n" or @pt="vnw") and not (%Rpronoun%) and @rel="obj1"] and not(node[@pt="vz" and @vztype="fin"]))]'
vzn1xpath = expandmacros(vzn1basexpath)
vzn2xpath = './/node[node[@lemma="in" and @rel="mwp"] and node[@lemma="deze" and @rel="mwp"]]'
vzn3xpath = './/node[@pt="vz" and ../node[(@lemma="dit" or @lemma="dat")  and @begin=../node[@pt="vz"]/@end and count(node)<=3] ]'
# vzn4basexpath = './/node[node[@pt="vz" and @rel="hd" and ../node[%Rpronoun% and @rel="obj1" and @end <= ../node[@rel="hd"]/@begin]]]'
# vzn4xpath = expandmacros(vzn4basexpath)


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
    # results += stree.xpath(vzn4xpath) # does not belong here after all, these will be scored under Vo/Bij
    return results
