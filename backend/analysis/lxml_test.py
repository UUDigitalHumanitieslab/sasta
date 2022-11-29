from sastadev.macros import expandmacros
from lxml import etree
import pytest


@pytest.fixture
def expected_results():
    return [[],
            [('top', '0', '8'), ('du', '0', '7'), ('pp', '4', '7'), ('np', '5', '7')],
            [('top', '0', '8'), ('du', '0', '7'), ('pp', '4', '7'), ('np', '5', '7')],
            [('smain', '1', '7')],
            [('smain', '1', '7')],
            [],
            [('smain', '1', '7')],
            [], [], [], [], [], [], [], [], [], [], []]


@pytest.fixture
def strees():
    streestrings = {}
    streestrings[0] = """
    <alpino_ds version="1.6">
      <parser cats="1" skips="0" />
      <node begin="0" cat="top" end="8" id="0" rel="top">
        <node begin="0" cat="du" end="7" id="1" rel="--">
          <node begin="0" conjtype="neven" end="1" frame="complementizer(root)" his="normal" his_1="normal" id="2" lcat="du" lemma="en" pos="comp" postag="VG(neven)" pt="vg" rel="dlink" root="en" sc="root" sense="en" word="en"/>
          <node begin="1" cat="smain" end="7" id="3" rel="nucl">
            <node begin="1" end="2" frame="tmp_adverb" his="normal" his_1="normal" id="4" lcat="advp" lemma="toen" pos="adv" postag="BW()" pt="bw" rel="mod" root="toen" sense="toen" special="tmp" word="toen"/>
            <node begin="2" end="3" frame="verb(hebben,past(sg),ld_pp)" his="normal" his_1="normal" id="5" infl="sg" lcat="smain" lemma="zitten" pos="verb" postag="WW(pv,verl,ev)" pt="ww" pvagr="ev" pvtijd="verl" rel="hd" root="zit" sc="ld_pp" sense="zit" stype="declarative" tense="past" word="zat" wvorm="pv"/>
            <node begin="3" case="nom" def="def" end="4" frame="pronoun(nwh,thi,sg,de,nom,def)" gen="de" genus="masc" getal="ev" his="normal" his_1="normal" id="6" lcat="np" lemma="hij" naamval="nomin" num="sg" pdtype="pron" per="thi" persoon="3" pos="pron" postag="VNW(pers,pron,nomin,vol,3,ev,masc)" pt="vnw" rel="su" rnum="sg" root="hij" sense="hij" status="vol" vwtype="pers" wh="nwh" word="hij"/>
            <node begin="4" cat="pp" end="7" id="7" rel="ld">
              <node begin="4" end="5" frame="preposition(in,[])" his="normal" his_1="normal" id="8" lcat="pp" lemma="in" pos="prep" postag="VZ(init)" pt="vz" rel="hd" root="in" sense="in" vztype="init" word="in"/>
              <node begin="5" cat="np" end="7" id="9" rel="obj1">
                <node begin="5" end="6" frame="determiner(de)" his="normal" his_1="normal" id="10" infl="de" lcat="detp" lemma="de" lwtype="bep" naamval="stan" npagr="rest" pos="det" postag="LID(bep,stan,rest)" pt="lid" rel="det" root="de" sense="de" word="de"/>
                <node begin="6" end="7" frame="noun(both,both,both)" gen="both" genus="zijd" getal="ev" graad="basis" his="noun" id="11" lcat="np" lemma="weiland" naamval="stan" ntype="soort" num="both" pos="noun" postag="N(soort,ev,basis,zijd,stan)" pt="n" rel="hd" rnum="sg" root="weiland" sense="weiland" word="weiland"/>
              </node>
            </node>
          </node>
        </node>
        <node begin="7" end="8" frame="punct(punt)" his="normal" his_1="normal" id="12" lcat="punct" lemma="." pos="punct" postag="LET()" pt="let" rel="--" root="." sense="." special="punt" word="."/>
      </node>
      <sentence sentid="42">en toen zat hij in de weiland .</sentence>
    <metadata>
    <meta type="text" name="charencoding" value="UTF8" />
    <meta type="text" name="childage" value="9;6" />
    <meta type="int" name="childmonths" value="114" />
    <meta type="text" name="comment" value="##META text title = STAP_04" />
    <meta type="text" name="session" value="STAP_04" />
    <meta type="text" name="origutt" value="en toen zat hij in de weiland." />
    <meta type="text" name="parsefile" value="Unknown_corpus_STAP_04_u00000000042.xml" />
    <meta type="text" name="speaker" value="CHI" />
    <meta type="int" name="uttendlineno" value="90" />
    <meta type="int" name="uttid" value="42" />
    <meta type="int" name="uttstartlineno" value="90" />
    <meta type="text" name="name" value="chi" />
    <meta type="text" name="SES" value="" />
    <meta type="text" name="age" value="9;6" />
    <meta type="text" name="custom" value="" />
    <meta type="text" name="education" value="" />
    <meta type="text" name="group" value="" />
    <meta type="text" name="language" value="nld" />
    <meta type="int" name="months" value="114" />
    <meta type="text" name="role" value="Target_Child" />
    <meta type="text" name="sex" value="male" />
    <meta type="text" name="xsid" value="42" />
    <meta type="int" name="uttno" value="42" />
    </metadata>
    </alpino_ds>"""

    strees = {}
    for el in streestrings:
        strees[el] = etree.fromstring(streestrings[el])
    return strees


@pytest.fixture
def queries():
    bigquery = """//node[(
    %declarative%
    and
    %Ond%
    and
    %Tarsp_B_X_count% = 3
    )]"""

    queries = []
    queries.append('//node[%Tarsp_WVz_exception%]')
    queries.append('//node[count(node[@cat or @pt]) = 2]')
    queries.append('//node[count(node[@cat] |  node[@pt]) = 2]')
    queries.append('//node[( %declarative% )]')
    queries.append('//node[( %Ond%  )]')
    queries.append('//node[(   %Tarsp_B_X_count% = 3)]')
    # queries.append(bigquery)
    queries.append('//node[%declarative% and %Ond%]')
    queries.append('//node[%declarative% and %Tarsp_B_X_count% = 3]')
    queries.append('//node[%declarative% and (%Tarsp_B_X_count%) = 3]')
    queries.append('//node[%declarative% and (%Tarsp_B_X_count% = 3)]')
    queries.append('//node[%declarative% and ((%Tarsp_B_X_count%) = 3)]')
    queries.append('//node[%Ond% and %Tarsp_B_X_count% = 3]')
    queries.append('//node[%Ond% and (%Tarsp_B_X_count%) = 3]')
    queries.append('//node[%Ond% and (%Tarsp_B_X_count% = 3)]')
    queries.append('//node[( (%declarative%) and (%Ond%)  and  (%Tarsp_B_X_count% = 3))]')
    queries.append('//node[( (%declarative%) and (%Ond%)  and  (%Tarsp_B_X_count% = 3))]')
    queries.append('//node[( %declarative% and %Ond%  and  (%Tarsp_B_X_count%) = 3)]')
    queries.append(
        '//node[(%declarative% and %Ond% and %Tarsp_W% and %Tarsp_B_X_count% = 3 and %realcomplormodnodecount% = 4)]')

    return queries


@pytest.fixture
def fullqueries(queries):
    fullqueries = []
    for query in queries:
        expandedquery = expandmacros(query)
        fullqueries.append('.' + expandedquery)
    return fullqueries


def getresults(stree, fullquery):
    noderesults = stree.xpath(fullquery)
    results = []
    for noderesult in noderesults:
        cat = noderesult.get('cat')
        pos = noderesult.get('pt')
        poscat = pos if cat is None else cat
        begin = noderesult.get('begin')
        end = noderesult.get('end')
        result = (poscat, begin, end)
        results.append(result)
    return results


def test_lxml_version(queries, fullqueries, expected_results, strees):
    '''Some lxml versions raise problems with macro expansion
    This test should be succeed when changing lxml version,
    otherwise do NOT proceed. Will break analysis.'''

    for stree in strees:
        for _, fullquery, expected_result in zip(queries, fullqueries,
                                                 expected_results):
            results = getresults(strees[stree], fullquery)
            assert results == expected_result
