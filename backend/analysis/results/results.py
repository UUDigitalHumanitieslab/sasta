from typing import Counter, Dict, List, Match, Tuple, Union

from lxml import etree as ET
import logging

logger = logging.getLogger('sasta')

QueryTuple = Tuple[str, str]
SynTree = Union[ET._Element, str]
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


class Query:
    ''' SASTAdev query format.
        Mostly aligns with SASTA django model.
    '''
    sastadev_mapping = {'query_id': 'id', 'category': 'cat'}

    def __init__(self, id, cat, subcat, level, item, altitems, implies,
                 original, pages, fase, query, inform,
                 screening, process, special1, special2, comments):
        self.id = id
        self.cat = cat
        self.subcat = subcat
        self.level = level
        self.item = item
        self.altitems = altitems
        self.implies = implies
        self.original = original
        self.pages = pages
        self.fase = fase
        self.query = query
        self.inform = inform
        self.screening = screening
        self.process = process
        self.special1 = self.clean(special1)
        self.special2 = special2
        self.comments = comments

    def __repr__(self):
        return ('\n'.join([f'{k}: {v}' for k, v in vars(self).items()]))

    def clean(self, valstr):
        if valstr:
            return valstr.strip().lower()
        return valstr

    @ classmethod
    def from_model(cls, model):
        relevant_fields = [f for f in model._meta.fields
                           if f.get_internal_type()
                           not in ('AutoField', 'ForeignKey')]
        values = {f.name: getattr(model, f.name) for f in relevant_fields}

        for k, v in values.items():
            if k in cls.sastadev_mapping:
                values[cls.sastadev_mapping.get(k)] = values.pop(k)

        return cls(**values)
