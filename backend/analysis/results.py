from typing import Any, Counter, Dict, List, Match, Tuple

QueryTuple = Tuple[str, str]
# TODO: XPath syntree type
SynTree = Any
SastaMatch = Tuple[Match, SynTree]
SastaMatchList = List[SastaMatch]
SastaMatches = Tuple[QueryTuple, SastaMatchList]
SastaResults = Dict[str, Counter[str]]


class AllResults:
    def __init__(self,
                 uttcount: int,
                 coreresults: SastaResults,
                 postresults: SastaResults,
                 allmatches: SastaMatches,
                 filename: str):
        self.uttcount = uttcount
        self.coreresults = coreresults
        self.postresults = postresults
        self.allmatches = allmatches
        self.filename = filename
