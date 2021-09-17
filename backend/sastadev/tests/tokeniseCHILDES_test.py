from sastadev.tokeniseCHILDES import tokenise


def test_tokenise_childes():
    teststrs = ['*CHI:	hij zei dat xxx [: genoeg van de weg] heeft .', 'dit (i)s <een een> [//] zinnetje!']

    for zin in teststrs:
        toklist = tokenise(zin)
        print(toklist)
