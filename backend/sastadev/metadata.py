from lxml import etree

bpl_none, bpl_word, bpl_node, bpl_delete = tuple(range(4))
defaultpenalty = 10
defaultbackplacement = bpl_none

SASTA = 'SASTA'

xmlformat = '''
<xmeta name="{name}" type="{atype}" value= "{value}" annotationwordlist="{annotationwordlist}"
       annotationposlist="{annotationposlist}" annotatedwordlist="{annotatedwordlist}"
       annotatedposlist="{annotatedposlist}"  cat="{cat}" subcat="{subcat}" source="{source}"
       backplacement="{backplacement}" penalty="{penalty}"
/>
'''


class Meta:
    def __init__(self, name, value, annotationwordlist=[], annotationposlist=[], annotatedposlist=[],
                 annotatedwordlist=[], atype='text', cat=None, subcat=None, source=None, penalty=defaultpenalty,
                 backplacement=defaultbackplacement):
        self.atype = atype
        self.name = name
        self.annotationwordlist = annotationwordlist if annotationwordlist != [] else value
        self.annotationposlist = annotationposlist
        self.annotatedwordlist = annotatedwordlist
        self.annotatedposlist = annotatedposlist
        self.value = value
        self.cat = cat
        self.subcat = subcat
        self.source = source
        self.penalty = penalty
        self.backplacement = backplacement
        self.fmstr = '<{}:type={}:annotationwordlist={}:annotationposlist={}:annotatedwordlist={}:annotatedposlist={}:value={}:cat={}:source={}>'
        self.xmlformat = xmlformat

    def __repr__(self):
        reprfmstr = 'Meta({},{},annotationwordlist={},annotationposlist={},annotatedposlist{},annotatedwordlist={},' \
                    ' atype={}, cat={}, subcat={}, source={}, penalty={}, backplacement={})'
        result = reprfmstr.format(repr(self.name), repr(self.value), repr(self.annotationwordlist), repr(self.annotationposlist),
                                  repr(self.annotatedposlist), repr(self.annotatedwordlist), repr(self.atype),
                                  repr(self.cat), repr(self.subcat), repr(self.source), repr(self.penalty), repr(self.backplacement))
        return result

    def __str__(self):
        frm = self.fmstr.format(self.name, self.atype, str(self.annotationwordlist),
                                str(self.annotationposlist), str(self.annotatedwordlist), str(self.annotatedposlist),
                                str(self.value), str(self.cat), str(self.source))
        return frm

    def toElement(self):
        # result = self.xmlformat.format(name=self.name, atype=self.atype, annotationwordlist=str(self.annotationwordlist),
        #                    annotationposlist=str(self.annotationposlist), annotatedwordlist=str(self.annotatedwordlist),
        #                    annotatedposlist=str(self.annotatedposlist), value=str(self.value), cat=str(self.cat),
        #                         subcat=self.subcat,  source=str(self.source), backplacement=self.backplacement,
        #                         penalty=self.penalty)

        result = etree.Element('xmeta', name=self.name, atype=self.atype, annotationwordlist=str(self.annotationwordlist),
                               annotationposlist=str(self.annotationposlist), annotatedwordlist=str(self.annotatedwordlist),
                               annotatedposlist=str(self.annotatedposlist), value=str(self.value), cat=str(self.cat),
                               subcat=str(self.subcat), source=str(self.source), backplacement=str(self.backplacement),
                               penalty=str(self.penalty))
        return result


def selectmeta(name, metadatalist):
    for meta in metadatalist:
        if meta.name == name:
            return meta
    return None


def mkSASTAMeta(token, nwt, name, value, cat, subcat=None, penalty=defaultpenalty, backplacement=defaultbackplacement):
    result = Meta(name, value, annotatedposlist=[token.pos],
                  annotatedwordlist=[token.word], annotationposlist=[nwt.pos],
                  annotationwordlist=[nwt.word], cat=cat, subcat=subcat, source=SASTA, penalty=penalty,
                  backplacement=backplacement)
    return result
