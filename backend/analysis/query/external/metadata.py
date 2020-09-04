class Meta:
    def __init__(self,  name, value, annotationposlist=[], annotatedposlist=[], annotatedwordlist=[], atype='text'):
        self.atype = atype
        self.name = name
        self.annotationposlist = annotationposlist
        self.annotatedwordlist = annotatedwordlist
        self.annotatedposlist = annotatedposlist
        self.value = value

    def __str__(self):
        frm = '<{}:type={}:annotationwordlist=value={}:annotationposlist={}:annotatedwordlist={}:annotatedposlist={}>'.format(
            self.name, self.atype, self.value, str(self.annotationposlist), str(self.annotatedwordlist), str(self.annotatedposlist))
        return frm
