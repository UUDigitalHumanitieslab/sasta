import re

#anonymisation codes
#these are provided in the order they should be checked. Note that PLAATSNAAM will match as a place, not a person
ANONYMIZATIONS = [
                    {
                        'category' : 'place',
                        'codes': ['PLAATS', 'PLAATSNAAM'], 
                        'common': ['Utrecht', 'Breda', 'Leiden', 'Maastricht', 'Arnhem']
                    },
                    {
                        'category': 'person',
                        'codes': ['NAAM', 'BROER', 'ZUS', 'KIND'], 
                        'common': ['Maria', 'Jan', 'Anna', 'Esther', 'Pieter', 'Sam']
                    } 
                ]

def fill_name(string):
    for specs in ANONYMIZATIONS:
        codes =  '|'.join(sorted(specs['codes'], key=len, reverse=True))
        # groups: 1) word boundary 2) code 3) counter 4) word boundary
        pat = fr'(\b)\w*({codes})[^\d\W]*(\d*)(\b)'
        match = re.search(pat, string)

        def repl(match):
            try:
                index = int(match.group(3))
            except (IndexError, ValueError):
                index = 0
            repl = specs['common'][index]
            return match.group(1) + repl + match.group(4)

        if match:
            newstring = re.sub(pat, repl, string, count=1)
            index = match.start()
            old = match.group(0)
            new = repl(match)
            comment = "{}|{}|{}".format(index, old, new)
            return newstring, comment
        
    #if no replacements were made, return original with no comment
    return string, None


def correct_punctuation(string):
    #replace ellipses
    #pattern: matches all '...' and '…' except when preceded by '+' or surrounded by '(' and ')'
    pattern = r'(?<!\+)(…|\.{3})(?!\))|(?<!\()(?<!\+)(…|\.{3})'
    match = re.search(pattern, string)
    if match:
        index = match.start()
        old = match.group(0)
        new = '+...'
        newstring = re.sub(pattern, new, string, count=1)
        comment = '{}|{}|{}'.format(index, old, new)
        return newstring, comment

    #replace hashtag
    pattern = r'#'
    match = re.search(pattern, string)
    if match:
        index = match.start()
        old = match.group()
        new = '(.)'
        newstring = re.sub(pattern, new, string, count=1)
        comment = '{}|{}|{}'.format(index, old, new)
        return newstring, comment

    #flag parentheses
    #pauses (.), (..) and (...) are okay, anything else should raise an error
    pauses_removed = re.sub(r'\(\.{1,3}\)', '', string)
    if '(' in pauses_removed or ')' in pauses_removed:
        raise ValueError('Parentheses in utterances are not allowed.')
        
    #if no replacements were made, return original with no comment
    return string, None