from sastadev import sastatok
from sastadev.cleanCHILDEStokens import space, scope_open, cleantext


def test_nesting():
    teststr = {}
    testlist = [r'eerst < een heel> [/] een hele simpele < test > [//] proef ',
                r'een test < <begin eens> [/] opnieuw en dan < nog eens> [/] opnieuw > [/] opnieuw hoor !',
                r'dat < kan> [/] is &he iets [/] en < ja <nog me> [//] nog meer > [: ik heb nog meer] te doen> hoor!',
                u'Dit een \u201Cquote en een \u2018inner quote\u2019 er ook nog bij\u201D ja en  los \u201D en \u2019 ja +..',
                r' en [%xxx: wat is dat ] &eh www[>] maar mooi@a en [<] lelijk@x en myown@z:xxx en mooi [=? kooi] <heel iets> [?] anders',
                r'en < scope scopeend > [:: test] klaar',
                r'Das [: dat ] mooi@a een [/] een en < scope scopeend > [:: test] en [=? x] wat [?] helemaal opnieuw [///] drie [x 3 ] mooi [= beautiful] en dan [% commentaar ]',
                r'Das [: dat is ] is  @ab xxx en <Pikkie Paus> [: Mickey Mouse] en  &+uh en  (ge)kocht  klaar '
                ]
    i = 0
    for el in testlist:
        teststr[i] = el
        i += 1

    for i in teststr:
        print(teststr[i])
        intokens = sastatok.sasta_tokenize(teststr[i])
        intokenstrings = [str(token) for token in intokens]
        print(space.join(intokenstrings))
        tokenctr = 0
        while tokenctr < len(intokens):
            (ob, oe, results) = (None, None, [])
            if intokens[tokenctr].word == scope_open:
                (ob, oe, results) = findfirstnestings(intokens[tokenctr:])
                print(ob, oe)
                for el in results:
                    print(el)
                print('')
            if oe is not None:
                tokenctr = oe + 1
            else:
                tokenctr += 1


def test_full():
    repkeep = True
    teststr = {}
    shorttestlist = ['·%pic: cat.jpg·', 'dit [/] dat', 'dit [/]', '[/] dat', '[?]', 'aap [?]', 'aap [?] mies',
                     'dit [/] dit [/] dit', '<dit duurt lang> ·0_1073·', 'mooi ·0_1073·', '·0_1073·',
                     '↫b-b-b↫boy', 'ba↫na-na↫nana', 'This is a ba [/] \u02CCba:\u02C8na:^na [?]',
                     '[- eng] this is my juguete@s.',
                     r'een test < <begin eens> [/] opnieuw en dan < nog eens> [/] opnieuw > [/] opnieuw hoor !',
                     r' een < wee > [/] weet ik',
                     r'eerst < een heel> [/] een hele simpele < test > [//] proef ',
                     u'Dit een \u201Cquote en een \u2018inner quote\u2019 er ook nog bij\u201D ja en  los \u201D en \u2019 ja +..',
                     r' hier is een (.) pauze, een langere (..), nog een langere (...) en een getimede (3.6) hier',
                     r'dan nu wee [/?] weet ik [^c] dit is 0een ^nie nieuwe &*LAU:hmm clause',
                     r' en [%xxx: wat is dat ] &eh www[>] maar mooi@a en [<] lelijk@x en myown@z:xxx en mooi [=? kooi] <heel iets> [?] anders',
                     r'en < scope scopeend > [:: test] klaar',
                     r'Das [: dat ] mooi@a een [/] een en < scope scopeend > [:: test] en [=? x] wat [?] helemaal opnieuw [///] drie [x 3 ] mooi [= beautiful] en dan [% commentaar ]'
                     r'Das [: dat is ] is  @ab xxx en <Pikkie Paus> [: Mickey Mouse] en  &+uh en  (ge)kocht  klaar ',
                     r'Das [: dat is ] is een [/] een <ja een> [/] ja een @ab xxx en <Pikkie Paus> [: Mickey Mouse] en yyy en www  maar &+uh en [/] (ge)kocht boeke(n) ei(gen)lijk klaar ',
                     r'Dat [:: dit] (i)s 0toch &he niet [x 3] zo efoudig [: eenvoudig], hoor!',
                     r'Dat (i)s 0toch &he niet [x 3] zo efoudig [: heel eenvoudig], hoor!',
                     r'Nu <een of twee> [=? een twee] of toch [?] <heel iets> [?] anders',
                     r'ja <ik wil> [/] ik wil graag doch [//] toch iest [: iets] anders [% commentaar] doen',
                     r'dat < kan &he iets >[/] en < ja <nog me> [//] nog meer > te doen> hoor!',
                     r'eerst < een heel> [/] een hele simpele < test > [//] proef ',
                     r'een test < <begin eens> [/] opnieuw en dan < nog eens> [/] opnieuw > [/] opnieuw hoor !',
                     r'dat < kan> [/] is &he iets [/] en < ja <nog me> [//] nog meer > [: ik heb nog meer] te doen> hoor!',
                     u'Dit een \u201Cquote en een \u2018inner quote\u2019 er ook nog bij\u201D ja en  los \u201D en \u2019 ja +..',
                     r' en [%xxx: wat is dat ] &eh www[>] maar mooi@a en [<] lelijk@x en myown@z:xxx en mooi [=? kooi] <heel iets> [?] anders',
                     r'en < scope scopeend > [:: test] klaar',
                     r'Das [: dat ] mooi@a een [/] een en < scope scopeend > [:: test] en [=? x] wat [?] helemaal opnieuw [///] drie [x 3 ] mooi [= beautiful] en dan [% commentaar ]',
                     r'Das [: dat is ] is  @ab xxx en <Pikkie Paus> [: Mickey Mouse] en  &+uh en  (ge)kocht  klaar '
                     ]
    shorttestlist += ['(s)pele(n)', 'spele(n)', 'e(n)', 'e(n) nu (s)pele(n) maar', 'e(n) nu kinneboejij [: kinderboerderij] (s)pele(n)']
    shorttestlist += ['<ja ja> [=! singing] .']
    shorttestlist += ['en waar is (he)t paard ?']
    shorttestlist += ['en toen plonsde [een] hij &+z in het water .']
    shorttestlist += ['en dat was het . [+bch]']
    shorttestlist += ['en dat was het . [+trn]']
    shorttestlist += ['&-eh en toen ging de buschauffeur [:bus] verder rijden .', '&-eh en toen ging de buschauffeur [:: bus] verder rijden .', '&-eh en toen ging de buschauffeur [: bus] verder rijden .']
    shorttestlist += ['want die wou er helemaal &+n niet meer rijden op+...']
    shorttestlist += ['<&mu [/] moe(t) je> [//] &k [/] kan je met deur dat doen ?']
    shorttestlist += ['Diekie [: Dikkie (Dik)].', 'Steven een boken@d [: boke@d] eten .']
    shorttestlist += ['ikke [/] (.) ikke <in s> [/] +...']
    shorttestlist += ['en [/] en <toen> [/] ↫t↫ toen hij gewonnen had toen <↫g↫ ging> [//] 	reed hij langs een tunnel waar de trein weer wegging . 36866_48162']
    shorttestlist += [' ging &jiks [*] [//] Jiska even kijken ?', ' ging <&jiks [*]> [//] Jiska even kijken ?']
    shorttestlist += ['<nu sij> [= nu zijn <we er>].']
    shorttestlist += ['www [>] .']
    shorttestlist += ['book [*] [/] boek', 'book [* p:r] [/] boek']
    shorttestlist += ['&=crying [<] .']
    shorttestlist += ['‹papier ,› heleboel papier . 53796_57231', '0 .']
    shorttestlist += ['ikke [/] (.) ikke <in s> [/] +...', '0', '0.', 'ik 0doe iets', '0 [% kicks the ball] .',
                      '&=imit:motor', ' boek[e]', 'boek [e]'  '<dit weg> [e] dit blijft',
                      '\u2039dit niet\u203a dit wel', '\u2039 dit niet \u203a dit wel', 'ik ze:g: maar : dat is goed']
    shorttestlist += ['ja , ik vind <dat zo leuk <dat het> [/]> [>] dat het blijft staan .', '<even on [/] > [<] onderbroek aan .']
    shorttestlist += ['wat is die [>] [//] +/.']
    shorttestlist += ['<is dit> [?] [//] <die is> [//] eh deze voor (.) voor Paulien .',
                      'op die deur <heeft alles> [!] [//] heeft Daan gemaakt , wat op de deur hangt .',
                      'hier< zo> [?] [/] zo moet ie .', 'ris [=? er is] [/] ris ie niet Koekiemonster ris ris .',
                      '&=hug:Rosa wat is er , moet jij naar bed ?',
                      '+, i i ik &jijk &jijk [/] <ik ook ə> [//] <ik ə> [/] <ik ə> [//] ik ook hebben <ook hebben> [//] <ik ə ook> [//] +/.']
    shorttestlist += ['<<dit die> [/] <dit die> [/]> [<] die [/] die [//] ditte pepot ?',
                      '<en de [//]> [<] en nog stoomboot <is dit> [>] .', 'rust [!] [//] Daan [>] .',
                      'en dan gaat lekker het eendje gaat +..?']
    shorttestlist += ['maar [/] maar <de &+b> [/] de bus was kapot . 26393_29792']
    shorttestlist += ['hebben schoene ---.']
    shorttestlist = ['uh mijn be-roep is een uh uh actie nee ak ak nee – activiteiten nee &=laughs euh goh', 'nou  ik denk <is>  +...']
    testlist = shorttestlist
    i = 0
    for el in testlist:
        teststr[i] = el
        i += 1

    for i in teststr:
        print(i, teststr[i])
        intokens = sastatok.sasta_tokenize(teststr[i])
        intokenstrings = [str(token) for token in intokens]
        print(space.join(intokenstrings))
        (newtokens, metadata) = cleantext(teststr[i], repkeep)
        tokenstrings = [str(token) for token in newtokens]
        print(space.join(tokenstrings))
        # mdstrs = [str(m) for m in metadata]
        # print(space.join(mdstrs))
        for m in metadata:
            print(str(m))
        print('')


def test_chat():
    repkeep = False
    infilename = 'chattest/chattestin/chattestutts.txt'
    infile = open(infilename, 'r', encoding='utf8')
    outfilename = 'chattest/chattestout/chattestutts.txt'
    outfile = open(outfilename, 'w', encoding='utf8')
    for utt in infile:
        print(utt, file=outfile)
        intokens = sastatok.sasta_tokenize(utt)
        intokenstrings = [str(token) for token in intokens]
        print(space.join(intokenstrings), file=outfile)
        (newtokens, metadata) = cleantext(utt, repkeep)
        tokenstrings = [str(token) for token in newtokens]
        print(space.join(tokenstrings), file=outfile)
        for m in metadata:
            print(str(m), file=outfile)
        print('', file=outfile)
