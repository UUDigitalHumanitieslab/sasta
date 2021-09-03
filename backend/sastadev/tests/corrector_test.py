from sastadev.corrector import (getalternatives, getcorrection, mkchatutt,
                                space)
from sastadev.tokeniseCHILDES import tokenise


def test_token():
    testutts = ['in het uh hier in het Breda uh silahe', 'Gaatie gaatie jaaaa, dat zijn mouwe met stukkies in de am-bu-lan-ce met de kopje thee']
    testutts += ['ieduleen [: iedereen] lettu [: redden].	iedereen redden .']
    testutts += ['ieduleen [: iedereen] lettu [: redden].	iedereen redden . Mama mouwe hoog']
    testutts += ['de bal']
    testutts += ['dat eh is mooi']
    testutts += ['de zwembad', 'de eh zwembad', 'de ja man']
    testutts += ['dit --- is -- een - hyphen test']
    testutts += ['hebbe een boek']
    testutts += ['hebbe schoene']
    testutts += ['die dich(t)']
    testutts += ['de kopje thee']
    testutts += ['en <ke [: de]> [//] hier nog ke [: de] babypaardje.']
    testutts += ['de kopje thee', 'ke [: de] babypaardje.', 'de ponyautootje']
    testutts += ['in de am-bu-lan-ce met', 'de kopje thee', 'Gaatie', 'gaatie', 'jaaaa', 'mouwe', 'stukkies']
    testutts += ['waar sit die zeep ?', 'iets erin setten', 'ie(t)s e(r)in setten.', 'ie(t)s e(r)in setten .']
    testutts += ['ie(t)s e(r)in setten.']
    testutts = ['kat-oorbellen.']

    for testutt in testutts:
        correction, metadata = getcorrection(testutt)
        print(testutt)
        print(space.join(correction))
        for metadatum in metadata:
            print(str(metadatum))


def test_corretor():
    testutts = ['in het uh hier in het Breda uh silahe', 'Gaatie gaatie jaaaa, dat zijn mouwe met stukkies in de am-bu-lan-ce met de kopje thee']
    for testutt in testutts:
        testtokens = tokenise(testutt)
        alternatives = getalternatives(testtokens, None, 0)
        # for el in alternatives:
        #    print(testtokens[el], space.join(alternatives[el]))
        # outputalternatives(testtokens, alternatives, sys.stdout)
        print(space.join(testtokens))
        for alternative in alternatives:
            print(space.join(alternative))
            chatutt = mkchatutt(testtokens, alternative.word)
            print(space.join(chatutt))
