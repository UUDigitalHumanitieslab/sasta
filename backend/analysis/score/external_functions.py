# from .compounds.compounds import iscompound


def getcompounds(syntree):
    results = []
    tlist = syntree.xpath(".//node[@pt]")
    for t in tlist:
        w = t.get('word')
        pt = t.get('pt')
        # if pt == 'n' and iscompound(w):
        # if pt == 'n':
        #     results.append(t)
    return results
