import logging
from operator import attrgetter
from typing import Callable, Dict, List, Union

from analysis.models import AssessmentMethod, AssessmentQuery
from analysis.results.results import UtteranceWord
from analysis.score.zc_embedding import get_zc_embeddings
from bs4 import BeautifulSoup as Soup
from django.db.models import Q
from lxml import etree as ET
from sastadev.external_functions import form_map, str2functionmap
from sastadev.macros import expandmacros, macrodict
from sastadev.query import Query

logger = logging.getLogger('sasta')


class QueryWithFunction:
    def __init__(self, query, function):
        self.id: str = query.id
        self.query: Query = query
        self.function: Union[Callable, ET.XPath] = function

    def __repr__(self):
        return f'{self.id}: {type(self.function)}'


# class Query:
#     ''' SASTAdev query format.
#         Mostly aligns with SASTA django model.
#     '''
#     sastadev_mapping = {'query_id': 'id', 'category': 'cat'}

#     def __init__(self, id, cat, subcat, level, item, altitems, implies,
#                  original, pages, fase, query, inform,
#                  screening, process, special1, special2, comments):
#         self.id = id
#         self.cat = cat or ''
#         self.subcat = subcat or ''
#         self.level = level or ''
#         self.item = item or ''
#         self.altitems = altitems or ''
#         self.implies = implies or ''
#         self.original = original
#         self.pages = pages or ''
#         self.fase = fase
#         self.query = query or ''
#         self.inform = inform
#         self.screening = screening
#         self.process = process
#         self.special1 = self.clean(special1)
#         self.special2 = self.clean(special2)
#         self.comments = comments or ''

#     def __repr__(self):
#         return ('\n'.join([f'{k}: {v}' for k, v in vars(self).items()]))

#     def clean(self, valstr):
#         if valstr:
#             return valstr.strip().lower()
#         return ''

#     @classmethod
#     def from_model(cls, model):
#         relevant_fields = [f for f in model._meta.fields
#                            if f.get_internal_type()
#                            not in ('AutoField', 'ForeignKey')]
#         values = {f.name: getattr(model, f.name) for f in relevant_fields}

#         for k, v in list(values.items()):
#             if k in cls.sastadev_mapping:
#                 values[cls.sastadev_mapping.get(k)] = values.pop(k)

#         return cls(**values)


def compile_queries(queries: List[Query]) -> List[QueryWithFunction]:
    results = []
    # macrodict = get_macros_dict()

    for query_model in queries:
        query = query_model.to_sastadev()
        func = compile_xpath_or_func(query.query, macrodict)
        if func:
            results.append(QueryWithFunction(query, func))
    return results


def compile_xpath_or_func(query: str,
                          macrodict: Dict) -> Union[Callable, ET.XPath]:
    try:
        if query in str2functionmap:
            return str2functionmap[query]
        expanded_query = expandmacros(query)
        return ET.XPath(expanded_query)
    except Exception as error:
        logger.warning(f'cannot compile {query.strip()}:\t{error}')
        return None


def filter_queries(method: AssessmentMethod,
                   phase: int = None,
                   phase_exact: bool = True):
    '''
    # TODO: remove phase filtering?
    phase_exact:True returns only that phase
                False returns everything up to (and including) that phase
    '''
    try:
        form_queries = [f.__name__ for f in form_map.values()]
        all_queries = AssessmentQuery.objects.all().filter(
            Q(method=method)
            & Q(query__isnull=False)
            & ~Q(query__exact='')
            & ~Q(query__in=form_queries)
            & Q(inform='yes')
        )
        if phase:
            phase_filter = Q(fase=phase) if phase_exact else Q(
                fase__gte=phase)
            phase_queries = all_queries.filter(phase_filter)
            return phase_queries
        return all_queries

    except Exception as e:
        logger.warning(f'cannot filter queries for phase:\t{e}')
        print(e)


def single_query_single_utt(query_func: Union[Callable, ET.XPath],
                            syntree: ET._Element) -> List[ET._Element]:
    try:
        results = query_func(syntree)
        return results
    except Exception:
        logger.warning(f'Failed to execute {query_func}')
        return []


def utt_from_tree(tree: str, embeddings=False) -> List[UtteranceWord]:
    # From a LASSY syntax tree, construct utterance representation
    # Output: sorted list of UtteranceWord instances
    soup = Soup(tree, 'lxml')
    utt = soup.alpino_ds

    embed_dict = get_zc_embeddings(ET.fromstring(tree)) if embeddings else None

    words = utt.findAll('node', {'word': True})

    unaligned = UtteranceWord(
        word='',
        begin=-1,
        end=0,
        hits=[],
        zc_embedding=0 if embed_dict else None
    )

    utt_words = [unaligned] + [UtteranceWord(
        word=w.get('word'),
        begin=w.get('begin'),
        end=w.get('end'),
        hits=[],
        zc_embedding=embed_dict[str(w.get('begin'))] if embed_dict else None)
        for w in words]

    # Sort the words and assign their real index
    sorted_words = sorted(utt_words, key=attrgetter('begin'))
    for i, w in enumerate(sorted_words):
        w.index = i

    return sorted_words
