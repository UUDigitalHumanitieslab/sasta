from sastadev import SDLOGGER

pre_process_str, core_process_str, post_process_str, form_process_str = 'pre', 'core', 'post', 'form'
pre_process, core_process, post_process, form_process = 0, 1, 2, 3


def getprocess(process):
    if process.lower() == core_process_str:
        result = core_process
    elif process.lower() == post_process_str:
        result = post_process
    elif process.lower() == pre_process_str:
        result = pre_process
    elif process.lower() == form_process_str:
        result = form_process
    else:
        result = -1
        SDLOGGER.error('Illegal value for process {}'.format(process))
    return result


def clean(valstr):
    result = valstr.strip().lower()
    return result


class Query:
    def __init__(self, id, cat, subcat, level, item, altitems, implies, original, pages, fase, query, inform,
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
        self.process = getprocess(process)
        self.special1 = clean(special1)
        self.special2 = special2
        self.comments = comments


def query_inform(query):
    result = query.inform == "yes"
    return result


def is_preorcore(query):
    result = is_pre(query) or is_core(query)
    return result


def is_pre(query):
    result = (query.process == pre_process)
    return result


def is_core(query):
    result = (query.process == core_process)
    return result


def is_post(query):
    result = (query.process == post_process)
    return result


def query_exists(query):
    result = query.query != "" and query.query is not None
    return result
