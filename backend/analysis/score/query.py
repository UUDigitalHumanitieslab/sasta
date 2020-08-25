from typing import Callable, List, Union, Dict
from analysis.models import AssessmentQuery
from analysis.macros.macros import get_macros_dict, expandmacros
from lxml import etree as ET
from analysis.score import external_functions
from analysis.results.results import UtteranceWord
from analysis.score.zc_embedding import get_zc_embeddings
from bs4 import BeautifulSoup as Soup
from operator import attrgetter

import logging
logger = logging.getLogger('sasta')


class QueryWithFunction:
    def __init__(self, query, function):
        self.id: str = query.id
        self.query: Query = query
        self.function: Union[Callable, ET.XPath] = function

    def __repr__(self):
        return f'{self.id}: {type(self.function)}'


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

    @classmethod
    def from_model(cls, model):
        relevant_fields = [f for f in model._meta.fields
                           if f.get_internal_type()
                           not in ('AutoField', 'ForeignKey')]
        values = {f.name: getattr(model, f.name) for f in relevant_fields}

        for k, v in values.items():
            if k in cls.sastadev_mapping:
                values[cls.sastadev_mapping.get(k)] = values.pop(k)

        return cls(**values)


def compile_queries(queries: List[AssessmentQuery]) -> List[QueryWithFunction]:
    results = []
    macrodict = get_macros_dict()
    for query_model in queries:
        query = Query.from_model(query_model)
        func = compile_xpath_or_func(query.query, macrodict)
        if func:
            results.append(QueryWithFunction(query, func))
    return results


def compile_xpath_or_func(query: str,
                          macrodict: Dict) -> Union[Callable, ET.XPath]:
    try:
        if query in dir(external_functions):
            return getattr(external_functions, query)
        expanded_query = expandmacros(query, macrodict)
        return ET.XPath(expanded_query)
    except Exception as error:
        logger.warning(f'cannot compile {query.strip()}:\t{error}')
        return None


def utt_from_tree(tree: str, embeddings=False) -> List[UtteranceWord]:
    # From a LASSY syntax tree, construct utterance representation
    # Output: sorted list of UtteranceWord instances
    soup = Soup(tree, 'lxml')
    utt = soup.alpino_ds

    if embeddings:
        embed_dict = get_zc_embeddings(ET.fromstring(tree))

    words = utt.findAll('node', {'word': True})
    utt_words = [UtteranceWord(
        word=w.get('word'),
        begin=w.get('begin'),
        end=w.get('end'),
        hits=[],
        zc_embedding=embed_dict[str(w.get('begin'))] if embed_dict else None)
        for w in words]

    return sorted(utt_words, key=attrgetter('begin'))
