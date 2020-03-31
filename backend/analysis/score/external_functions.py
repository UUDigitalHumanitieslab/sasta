from ..models import Compound


def getcompounds(syntree):
    results = []
    tlist = syntree.xpath(".//node[@pt]")
    for t in tlist:
        w = t.get('word')
        pt = t.get('pt')
        if pt == 'n' and iscompound(w):
            results.append(t)
    return results


def iscompound(string):
    if '_' in string:
        return True
    else:
        return Compound.objects.filter(HeadDiaNew=string.lower()).exists()
