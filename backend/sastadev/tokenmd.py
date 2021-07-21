class TokenListMD():
    def __init__(self, tokens, metadata):
        self.tokens = tokens
        self.metadata = metadata

    def __repr__(self):
        tokstr = repr(self.tokens)
        mdstr = repr(self.metadata)
        result = 'TokenMD({},{})'.format(tokstr, mdstr)
        return result


class TokenMD():
    def __init__(self, token, metadata):
        self.token = token
        self.metadata = metadata

    def __repr__(self):
        tokstr = repr(self.token)
        mdstr = repr(self.metadata)
        result = 'TokenMD({},{})'.format(tokstr, mdstr)
        return result


def mdlist2listmd(mdlist):
    newtokens = []
    mergedmetadata = []
    for tokenmd in mdlist:
        newtokens.append(tokenmd.token)
        mergedmetadata += tokenmd.metadata
    result = TokenListMD(newtokens, mergedmetadata)
    return result
