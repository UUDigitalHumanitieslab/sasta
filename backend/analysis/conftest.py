import glob
import json
import os.path as op

import pytest
from analysis.convert.convert import convert
from analysis.models import (AnalysisRun, AssessmentMethod, Corpus,
                             MethodCategory, Transcript)
from django.conf import settings
from django.core.files import File
from parse.parse_utils import create_utterance_objects
from sastadev.conf import settings as sd_settings

CORRECTIONS_TARSP_5 = '''{"Insertion": [["23", "Insertion", "['ik']", "SASTA", "Small Clause Treatment", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"], ["23", "Insertion", "['wil']", "SASTA", "Small Clause Treatment", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"]], "Retracing": [["36", "Retracing", "['di', 'zij', 'hem']", "CHAT", "None", "None", "nee dat wat <di zij hem> [//] hij verkoopt.", "dat wat hij verkoopt ."]], "parsed_as": [["4", "parsed_as", "kan nog een dingetje eraan .", "SASTA", "Correction", "None", "ja kan no(g) een dingetje d(e)raan.", "kan nog een dingetje eraan ."], ["7", "parsed_as", "even kijken waar .", "SASTA", "Correction", "None", "effe kijken waar.", "even kijken waar ."], ["11", "parsed_as", "je moet dan eventjes erop zetten .", "SASTA", "Correction", "None", "je moet dan effjes erop zetten.", "je moet dan eventjes erop zetten ."], ["12", "parsed_as", "dan ga ik dit eventjes maken .", "SASTA", "Correction", "None", "dan ga ik dit effjes maken.", "dan ga ik dit eventjes maken ."], ["19", "parsed_as", "deze past nergens meer op .", "SASTA", "Correction", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["20", "parsed_as", "dan zetten we dit effje aan de kant .", "SASTA", "Correction", "None", "dan zetten we deze effje aan de kant.", "dan zetten we dit effje aan de kant ."], ["22", "parsed_as", "kijk hier hebben wij heel veel .", "SASTA", "Correction", "None", "ja kij(k) hier hebben wij heel veel.", "kijk hier hebben wij heel veel ."], ["23", "parsed_as", "ik wil eventjes passen ?", "SASTA", "Correction", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"], ["24", "parsed_as", "teil .", "SASTA", "Correction", "None", "klik.", "teil ."], ["28", "parsed_as", "trappetje .", "SASTA", "Correction", "None", "ja trarpje [: trappetje].", "trappetje ."], ["32", "parsed_as", "alleen maar worstjes .", "SASTA", "Correction", "None", "nee wee [: alleen] maar wortjes [: worstjes].", "alleen maar worstjes ."], ["36", "parsed_as", "dat wat hij verkoopt .", "SASTA", "Correction", "None", "nee dat wat <di zij hem> [//] hij verkoopt.", "dat wat hij verkoopt ."]], "Replacement": [["16", "Replacement", "['gaan']", "CHAT", "None", "None", "ander(s) kaat [: gaan] te [: de] tiern [: dieren] door 't hek lopen.", null], ["16", "Replacement", "['de']", "CHAT", "None", "None", "ander(s) kaat [: gaan] te [: de] tiern [: dieren] door 't hek lopen.", null], ["16", "Replacement", "['dieren']", "CHAT", "None", "None", "ander(s) kaat [: gaan] te [: de] tiern [: dieren] door 't hek lopen.", null], ["19", "Replacement", "['nergens']", "CHAT", "None", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["23", "Replacement", "['eventjes']", "CHAT", "None", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"], ["28", "Replacement", "['trappetje']", "CHAT", "None", "None", "ja trarpje [: trappetje].", "trappetje ."], ["30", "Replacement", "['parasol']", "CHAT", "None", "None", "&oeps de parasel [: parasol].", null], ["32", "Replacement", "['alleen']", "CHAT", "None", "None", "nee wee [: alleen] maar wortjes [: worstjes].", "alleen maar worstjes ."], ["32", "Replacement", "['worstjes']", "CHAT", "None", "None", "nee wee [: alleen] maar wortjes [: worstjes].", "alleen maar worstjes ."], ["33", "Replacement", "['worstje']", "CHAT", "None", "None", "kijk hier zit een wortje [: worstje] in.", null], ["34", "Replacement", "['staat']", "CHAT", "None", "None", "wat taat [: staat] hierop?", null]], "GrammarError": [["20", "GrammarError", "deheterror", "SASTA", "Error", "None", "dan zetten we deze effje aan de kant.", "dan zetten we dit effje aan de kant ."]], "Disambiguation": [["24", "Disambiguation", "Avoid unknown reading", "SASTA", "Lexicon", "None", "klik.", "teil ."]], "ExtraGrammatical": [["4", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja kan no(g) een dingetje d(e)raan.", "kan nog een dingetje eraan ."], ["19", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["22", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja kij(k) hier hebben wij heel veel.", "kijk hier hebben wij heel veel ."], ["28", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja trarpje [: trappetje].", "trappetje ."], ["32", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "nee wee [: alleen] maar wortjes [: worstjes].", "alleen maar worstjes ."], ["36", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "nee dat wat <di zij hem> [//] hij verkoopt.", "dat wat hij verkoopt ."]], "Phonological Fragment": [["8", "Phonological Fragment", "['&hoo']", "CHAT", "None", "None", "&hoo hij kom(t).", null], ["10", "Phonological Fragment", "['&oo']", "CHAT", "None", "None", "&oo hij fiet(st) niet meer.", null], ["15", "Phonological Fragment", "['&nie']", "CHAT", "None", "None", "hij kan &nie nie(t) meer daarheen (s)chuiven.", null], ["19", "Phonological Fragment", "['&de']", "CHAT", "None", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["19", "Phonological Fragment", "['&de']", "CHAT", "None", "None", "ja &de &de deze past nerke [: nergens] meer op.", "deze past nergens meer op ."], ["27", "Phonological Fragment", "['&uhh']", "CHAT", "None", "None", "&uhh wat i(s) dit ook alweer?", null], ["30", "Phonological Fragment", "['&oeps']", "CHAT", "None", "None", "&oeps de parasel [: parasol].", null]], "Informal Pronunciation": [["7", "Informal Pronunciation", "Alternative Pronunciation", "SASTA", "Pronunciation", "None", "effe kijken waar.", "even kijken waar ."], ["11", "Informal Pronunciation", "Alternative Pronunciation", "SASTA", "Pronunciation", "None", "je moet dan effjes erop zetten.", "je moet dan eventjes erop zetten ."], ["12", "Informal Pronunciation", "Alternative Pronunciation", "SASTA", "Pronunciation", "None", "dan ga ik dit effjes maken.", "dan ga ik dit eventjes maken ."]], "Insertion Token Mapping": [["23", "Insertion Token Mapping", "[None, None, 30, 50, 60]", "SASTA", "Token Mapping", "None", "fftje [: eventjes] passen?", "ik wil eventjes passen ?"]], "Alternative Pronunciation": [["4", "Alternative Pronunciation", "d-onset on er", "SASTA", "Pronunciation", "None", "ja kan no(g) een dingetje d(e)raan.", "kan nog een dingetje eraan ."]]}'''
CORRECTIONS_ASTA_16 = '{"Pause": [["15", "Pause", "[\'(..)\']", "CHAT", "None", "None", "uh (..) BEROEP1", "BEROEP1"], ["33", "Pause", "[\'(.)\']", "CHAT", "None", "None", "(.) ja (.) ja ik weet het niet", "ik weet het niet"], ["33", "Pause", "[\'(.)\']", "CHAT", "None", "None", "(.) ja (.) ja ik weet het niet", "ik weet het niet"], ["38", "Pause", "[\'(..)\']", "CHAT", "None", "None", "dat heb ik net nog gelezen (..)", null], ["45", "Pause", "[\'(..)\']", "CHAT", "None", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["45", "Pause", "[\'(..)\']", "CHAT", "None", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["46", "Pause", "[\'(..)\']", "CHAT", "None", "None", "ik uh (..) uh ik doe uh boekjes voor uh club geloof ik uh", "ik doe boekjes voor club geloof ik"], ["47", "Pause", "[\'(...)\']", "CHAT", "None", "None", "en uh (...) uh (.) uh sorry", "en"], ["47", "Pause", "[\'(.)\']", "CHAT", "None", "None", "en uh (...) uh (.) uh sorry", "en"]], "parsed_as": [["1", "parsed_as", "ik vind het beetje moeilijk om het goed te vertellen want ik heb een ongeluk gehad", "SASTA", "Correction", "None", "ja uh ik vind het beetje moeilijk om het goed te vertellen want ik heb een ongeluk gehad ", "ik vind het beetje moeilijk om het goed te vertellen want ik heb een ongeluk gehad"], ["4", "parsed_as", "en nu krijg ik te horen", "SASTA", "Correction", "None", "en uh nu krijg ik te horen", "en nu krijg ik te horen"], ["6", "parsed_as", "en verder het gaat redelijk denk ik", "SASTA", "Correction", "None", "en verder ja het gaat redelijk denk ik", "en verder het gaat redelijk denk ik"], ["7", "parsed_as", "ik ben eerst naar een ziekenhuis geweest een aantal weken", "SASTA", "Correction", "None", "oh ja sorry ja ik ben eerst uh naar een ziekenhuis geweest een aantal weken", "ik ben eerst naar een ziekenhuis geweest een aantal weken"], ["8", "parsed_as", "toen een aantal weken in een iets van zorg", "SASTA", "Correction", "None", "toen een aantal weken in een een iets van zorg ", "toen een aantal weken in een iets van zorg"], ["9", "parsed_as", "ik weet niet in uh( . )", "SASTA", "Correction", "None", "ik weet niet uh in uh(.)", "ik weet niet in uh( . )"], ["10", "parsed_as", "buiten is Breda", "SASTA", "Correction", "None", "uh buiten Breda ", "buiten is Breda"], ["13", "parsed_as", "en toen ik zo ver weer was ben ik naar hier gekomen", "SASTA", "Correction", "None", "en en toen ik zo ver weer was ben ik naar hier gekomen", "en toen ik zo ver weer was ben ik naar hier gekomen"], ["14", "parsed_as", "dat heet de ZORGINSTELLING1", "SASTA", "Correction", "None", "dat heet de uh ZORGINSTELLING1", "dat heet de ZORGINSTELLING1"], ["15", "parsed_as", "BEROEP1", "SASTA", "Correction", "None", "uh (..) BEROEP1", "BEROEP1"], ["16", "parsed_as", "is heel erg leuk", "SASTA", "Correction", "None", "ja is heel erg leuk ja", "is heel erg leuk"], ["20", "parsed_as", "en is ook leuk kon kinderen zo gezellig zo lief zo fijn", "SASTA", "Correction", "None", "en is ook leuk kon kinderen zo gezellig zo lief zo fijn ja", "en is ook leuk kon kinderen zo gezellig zo lief zo fijn"], ["21", "parsed_as", "en ook ouders heel goed contact", "SASTA", "Correction", "None", "ja en ook ouders heel goed contact", "en ook ouders heel goed contact"], ["22", "parsed_as", "kinderen worden gebracht", "SASTA", "Correction", "None", "ki kinderen worden gebracht", "kinderen worden gebracht"], ["23", "parsed_as", "en dan is het contact goed met de ouders", "SASTA", "Correction", "None", "en uh dan is het contact goed met de ouders", "en dan is het contact goed met de ouders"], ["25", "parsed_as", "en kinderen zijn fijn lief", "SASTA", "Correction", "None", "en kinderen zijn ja fijn lief", "en kinderen zijn fijn lief"], ["26", "parsed_as", "en voelen zich wel gelukkig bij ons", "SASTA", "Correction", "None", "en voelen zich wel uh voelen zich wel gelukkig bij ons", "en voelen zich wel gelukkig bij ons"], ["28", "parsed_as", "ik werk drie dagen", "SASTA", "Correction", "None", "oo uh uh ik werk drie dagen", "ik werk drie dagen"], ["29", "parsed_as", "ik begin ik om half acht tot ik denk tot zes uur", "SASTA", "Correction", "None", "ja ik begin ik om uh half acht tot ik denk tot zes uur ja", "ik begin ik om half acht tot ik denk tot zes uur"], ["30", "parsed_as", "toevallig hierachter", "SASTA", "Correction", "None", "ja toevallig hierachter    ", "toevallig hierachter"], ["31", "parsed_as", "kinderen met beperking", "SASTA", "Correction", "None", "uh kinderen met beperking", "kinderen met beperking"], ["33", "parsed_as", "ik weet het niet", "SASTA", "Correction", "None", "(.) ja (.) ja ik weet het niet", "ik weet het niet"], ["35", "parsed_as", "ik herken het", "SASTA", "Correction", "None", "ik ik herken het", "ik herken het"], ["36", "parsed_as", "daar ben ik veel geweest", "SASTA", "Correction", "None", "wauw daar ben ik veel geweest", "daar ben ik veel geweest"], ["37", "parsed_as", "ook hier de", "SASTA", "Correction", "None", "ook hier de uh", "ook hier de"], ["40", "parsed_as", "veel geweest voor", "SASTA", "Correction", "None", "veel geweest voor uh", "veel geweest voor"], ["42", "parsed_as", "net gekoppeld", "SASTA", "Correction", "None", "ja uh net gekoppeld", "net gekoppeld"], ["44", "parsed_as", "dus maar ben ik veel geweest maar ook als ik hier", "SASTA", "Correction", "None", "dus maar ben ik veel geweest maar ook als ik hier uh", "dus maar ben ik veel geweest maar ook als ik hier"], ["45", "parsed_as", "ik zing met oudere mensen", "SASTA", "Correction", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["46", "parsed_as", "ik doe boekjes voor club geloof ik", "SASTA", "Correction", "None", "ik uh (..) uh ik doe uh boekjes voor uh club geloof ik uh", "ik doe boekjes voor club geloof ik"], ["47", "parsed_as", "en", "SASTA", "Correction", "None", "en uh (...) uh (.) uh sorry", "en"]], "ExtraGrammatical": [["1", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ja uh ik vind het beetje moeilijk om het goed te vertellen want ik heb een ongeluk gehad ", "ik vind het beetje moeilijk om het goed te vertellen want ik heb een ongeluk gehad"], ["1", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja uh ik vind het beetje moeilijk om het goed te vertellen want ik heb een ongeluk gehad ", "ik vind het beetje moeilijk om het goed te vertellen want ik heb een ongeluk gehad"], ["4", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "en uh nu krijg ik te horen", "en nu krijg ik te horen"], ["6", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "en verder ja het gaat redelijk denk ik", "en verder het gaat redelijk denk ik"], ["7", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oh ja sorry ja ik ben eerst uh naar een ziekenhuis geweest een aantal weken", "ik ben eerst naar een ziekenhuis geweest een aantal weken"], ["7", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oh ja sorry ja ik ben eerst uh naar een ziekenhuis geweest een aantal weken", "ik ben eerst naar een ziekenhuis geweest een aantal weken"], ["7", "ExtraGrammatical", "Interjection", "SASTA", "Syntax", "None", "oh ja sorry ja ik ben eerst uh naar een ziekenhuis geweest een aantal weken", "ik ben eerst naar een ziekenhuis geweest een aantal weken"], ["7", "ExtraGrammatical", "Repeated ja, nee, nou", "SASTA", "Syntax", "Repetition", "oh ja sorry ja ik ben eerst uh naar een ziekenhuis geweest een aantal weken", "ik ben eerst naar een ziekenhuis geweest een aantal weken"], ["7", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "oh ja sorry ja ik ben eerst uh naar een ziekenhuis geweest een aantal weken", "ik ben eerst naar een ziekenhuis geweest een aantal weken"], ["8", "ExtraGrammatical", "Repeated word token", "SASTA", "Tokenisation", "Repetition", "toen een aantal weken in een een iets van zorg ", "toen een aantal weken in een iets van zorg"], ["9", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ik weet niet uh in uh(.)", "ik weet niet in uh( . )"], ["10", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "uh buiten Breda ", "buiten is Breda"], ["13", "ExtraGrammatical", "Repeated word token", "SASTA", "Tokenisation", "Repetition", "en en toen ik zo ver weer was ben ik naar hier gekomen", "en toen ik zo ver weer was ben ik naar hier gekomen"], ["14", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "dat heet de uh ZORGINSTELLING1", "dat heet de ZORGINSTELLING1"], ["15", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "uh (..) BEROEP1", "BEROEP1"], ["16", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja is heel erg leuk ja", "is heel erg leuk"], ["16", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja is heel erg leuk ja", "is heel erg leuk"], ["20", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "en is ook leuk kon kinderen zo gezellig zo lief zo fijn ja", "en is ook leuk kon kinderen zo gezellig zo lief zo fijn"], ["21", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja en ook ouders heel goed contact", "en ook ouders heel goed contact"], ["22", "ExtraGrammatical", "Short Repetition", "SASTA", "Tokenisation", "Repetition", "ki kinderen worden gebracht", "kinderen worden gebracht"], ["23", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "en uh dan is het contact goed met de ouders", "en dan is het contact goed met de ouders"], ["25", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "en kinderen zijn ja fijn lief", "en kinderen zijn fijn lief"], ["26", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "en voelen zich wel uh voelen zich wel gelukkig bij ons", "en voelen zich wel gelukkig bij ons"], ["26", "ExtraGrammatical", "Word token of a repeated word token sequence", "SASTA", "Tokenisation", "Repetition", "en voelen zich wel uh voelen zich wel gelukkig bij ons", "en voelen zich wel gelukkig bij ons"], ["26", "ExtraGrammatical", "Word token of a repeated word token sequence", "SASTA", "Tokenisation", "Repetition", "en voelen zich wel uh voelen zich wel gelukkig bij ons", "en voelen zich wel gelukkig bij ons"], ["26", "ExtraGrammatical", "Word token of a repeated word token sequence", "SASTA", "Tokenisation", "Repetition", "en voelen zich wel uh voelen zich wel gelukkig bij ons", "en voelen zich wel gelukkig bij ons"], ["28", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oo uh uh ik werk drie dagen", "ik werk drie dagen"], ["28", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oo uh uh ik werk drie dagen", "ik werk drie dagen"], ["28", "ExtraGrammatical", "Interjection", "SASTA", "Syntax", "None", "oo uh uh ik werk drie dagen", "ik werk drie dagen"], ["29", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ja ik begin ik om uh half acht tot ik denk tot zes uur ja", "ik begin ik om half acht tot ik denk tot zes uur"], ["29", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja ik begin ik om uh half acht tot ik denk tot zes uur ja", "ik begin ik om half acht tot ik denk tot zes uur"], ["29", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja ik begin ik om uh half acht tot ik denk tot zes uur ja", "ik begin ik om half acht tot ik denk tot zes uur"], ["30", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja toevallig hierachter    ", "toevallig hierachter"], ["31", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "uh kinderen met beperking", "kinderen met beperking"], ["33", "ExtraGrammatical", "Repeated ja, nee, nou", "SASTA", "Syntax", "Repetition", "(.) ja (.) ja ik weet het niet", "ik weet het niet"], ["33", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "(.) ja (.) ja ik weet het niet", "ik weet het niet"], ["35", "ExtraGrammatical", "Repeated word token", "SASTA", "Tokenisation", "Repetition", "ik ik herken het", "ik herken het"], ["36", "ExtraGrammatical", "Interjection", "SASTA", "Syntax", "None", "wauw daar ben ik veel geweest", "daar ben ik veel geweest"], ["37", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ook hier de uh", "ook hier de"], ["40", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "veel geweest voor uh", "veel geweest voor"], ["42", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ja uh net gekoppeld", "net gekoppeld"], ["42", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "ja uh net gekoppeld", "net gekoppeld"], ["44", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "dus maar ben ik veel geweest maar ook als ik hier uh", "dus maar ben ik veel geweest maar ook als ik hier"], ["45", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["45", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["45", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["45", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["45", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["45", "ExtraGrammatical", "Interjection", "SASTA", "Syntax", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["45", "ExtraGrammatical", "ja, nee or nou filled pause", "SASTA", "Syntax", "None", "oo (..) uh ja uh uh (..) ik zing met uh oudere mensen uh", "ik zing met oudere mensen"], ["46", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ik uh (..) uh ik doe uh boekjes voor uh club geloof ik uh", "ik doe boekjes voor club geloof ik"], ["46", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ik uh (..) uh ik doe uh boekjes voor uh club geloof ik uh", "ik doe boekjes voor club geloof ik"], ["46", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ik uh (..) uh ik doe uh boekjes voor uh club geloof ik uh", "ik doe boekjes voor club geloof ik"], ["46", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ik uh (..) uh ik doe uh boekjes voor uh club geloof ik uh", "ik doe boekjes voor club geloof ik"], ["46", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "ik uh (..) uh ik doe uh boekjes voor uh club geloof ik uh", "ik doe boekjes voor club geloof ik"], ["46", "ExtraGrammatical", "Repeated word token", "SASTA", "Tokenisation", "Repetition", "ik uh (..) uh ik doe uh boekjes voor uh club geloof ik uh", "ik doe boekjes voor club geloof ik"], ["47", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "en uh (...) uh (.) uh sorry", "en"], ["47", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "en uh (...) uh (.) uh sorry", "en"], ["47", "ExtraGrammatical", "Filled Pause", "SASTA", "Syntax", "None", "en uh (...) uh (.) uh sorry", "en"], ["47", "ExtraGrammatical", "Interjection", "SASTA", "Syntax", "None", "en uh (...) uh (.) uh sorry", "en"]]}'


@pytest.fixture
def cha_testfiles_dir():
    return op.join(settings.BASE_DIR, 'test_files')


@pytest.fixture
def tarsp_category(db):
    obj = MethodCategory.objects.create(name='TARSP', zc_embeddings=True, levels=['Sz', 'Zc', 'Wg', 'VVW'], marking_postcodes=['[+ G]'])
    yield obj
    obj.delete()


@pytest.fixture
def stap_category(db):
    obj = MethodCategory.objects.create(name='STAP', zc_embeddings=False, levels=['Complexiteit', 'Grammaticale fout'], marking_postcodes=['[+ G]', '[+ VU]'])
    yield obj
    obj.delete()


@pytest.fixture
def asta_category(db):
    obj = MethodCategory.objects.create(name='ASTA', zc_embeddings=False, levels=[
        "Samplegrootte",
        "MLU",
        "Taalmaat",
        "Foutenanalyse",
        "Lemma"
    ], marking_postcodes=["[+ G]"])
    yield obj
    obj.delete()


@pytest.fixture
def method_dir():
    return op.join(sd_settings.SD_DIR, 'data', 'methods')


@pytest.fixture
def tarsp_method(db, tarsp_category, method_dir):
    file = glob.glob(f'{method_dir}/TARSP Index Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(name='tarsp_test_method', category=tarsp_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.fixture
def asta_method(db, asta_category, method_dir):
    file = glob.glob(f'{method_dir}/ASTA Index Current.xlsx')[0]
    with open(file, 'rb') as f:
        wrapped_file = File(f)
        instance = AssessmentMethod(name='asta_test_method', category=asta_category)
        instance.content.save(op.basename(file), wrapped_file)
    yield instance
    instance.delete()


@pytest.fixture
def tarsp_corpus(db, admin_user, tarsp_method, tarsp_category):
    obj = Corpus.objects.create(
        user=admin_user,
        name='tarsp_test_corpus',
        status='created',
        default_method=tarsp_method,
        method_category=tarsp_category
    )
    yield obj
    obj.delete()


@pytest.fixture
def asta_corpus(db, admin_user, asta_method, asta_category):
    obj = Corpus.objects.create(
        user=admin_user,
        name='asta_test_corpus',
        status='created',
        default_method=asta_method,
        method_category=asta_category
    )
    yield obj
    obj.delete()


@pytest.fixture
def tarsp_transcript(db, tarsp_corpus, cha_testfiles_dir):
    obj = Transcript.objects.create(
        name='tarsp_sample_5',
        status=Transcript.PARSED,
        corpus=tarsp_corpus
    )
    with open(op.join(cha_testfiles_dir, 'sample_5.cha'), 'rb') as f:
        obj.content.save('sample_5.cha', File(f))
    convert(obj)
    with open(op.join(cha_testfiles_dir, 'sample_5.xml'), 'rb') as f:
        obj.parsed_content.save('sample_5.xml', File(f))
    obj.corrections = json.loads(CORRECTIONS_TARSP_5)
    create_utterance_objects(obj)
    obj.save()
    yield obj
    obj.delete()


@pytest.fixture
def asta_transcript(db, asta_corpus, cha_testfiles_dir):
    obj = Transcript.objects.create(
        name='asta_sample_16',
        status=Transcript.PARSED,
        corpus=asta_corpus
    )
    with open(op.join(cha_testfiles_dir, 'sample_16.cha'), 'rb') as f:
        obj.content.save('sample_16.cha', File(f))
    convert(obj)
    with open(op.join(cha_testfiles_dir, 'sample_16.xml'), 'rb') as f:
        obj.parsed_content.save('sample_16.xml', File(f))
    obj.corrections = json.loads(CORRECTIONS_ASTA_16)
    create_utterance_objects(obj)
    obj.save()
    yield obj
    obj.delete()


@pytest.fixture
def asta_transcript_corrections(db, asta_transcript, asta_method, cha_testfiles_dir):
    obj = AnalysisRun(
        transcript=asta_transcript,
        method=asta_method,
        is_manual_correction=True
    )
    with open(op.join(cha_testfiles_dir, 'sample_16_SAF_corrected.xlsx'), 'rb') as f:
        obj.annotation_file.save('sample_16_SAF_corrected.xlsx', File(f))
    obj.save()
    yield obj
    obj.delete()
