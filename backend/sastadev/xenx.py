from .treebankfunctions import getattval, clausecats

CONJXPATH = './/node[@cat="conj" and (count(node)=3 or count(node)=5)]'


def getptcat(node):
    pt = getattval(node, 'pt')
    cat = getattval(node, 'cat')
    if pt != '':
        result = pt
    elif cat != '':
        result = cat
    else:
        result = None
    return result


def xenx(tree):
    results = []
    conjs = tree.xpath(CONJXPATH)
    for conj in conjs:
        include = True
        firstptcat = None
        crdresult = None
        for child in conj:
            childrel = getattval(child, 'rel')
            childptcat = getptcat(child)
            childlemma = getattval(child, 'lemma')
            if include:
                if childrel == 'crd':
                    include = include and (childlemma in ['en', 'of'])
                    crdresult = child
                elif childrel == 'cnj':
                    if childptcat is None:
                        include = False
                    if firstptcat is None:
                        firstptcat = childptcat
                    include = include and (childptcat == firstptcat) and childptcat not in clausecats
        if include:
            results.append(crdresult)
    return results
