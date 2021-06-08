commaspace = ', '


def checkinteger(thestr):
    try:
        cast = int(thestr)
        result = True
    except ValueError:
        result = False
    return result


def counter2list(thecounter):
    resultlist = []
    allintegers = True
    for el in thecounter:
        if allintegers:
            allintegers = allintegers and checkinteger(el)
        cnt = thecounter[el]
        for i in range(cnt):
            resultlist.append(str(el))
    if allintegers:
        sortedresultlist = sorted(resultlist, key=int)
    else:
        sortedresultlist = sorted(resultlist)
    return sortedresultlist


def counter2liststr(thecounter):
    thelist = counter2list(thecounter)
    result = commaspace.join(thelist)
    return result
