from typing import Counter, Dict, Optional, Tuple

# Type annotations
TupleStrDict = Dict[Tuple[Optional[str], Optional[str]], str]
CounterDict = Dict[str, Counter[str]]

# Global
ITEMSEPPATTERN = r'[,-; ]'
LABELSEP = ','
UTTLEVEL = 'utt'
HEADER_VARIANTS = {
    'speaker': ['speaker', 'spreker', 'spk'],
    'utt_id': ['id', 'utt', 'uttid'],
    'level': ['level'],
    'phase': ['fases', 'stages'],
    'comments': ['comments', 'commentaar']
}
PREFIX = ""
ALTITEMSEP = IMPLIESSEP = ','
SAF_COMMENT_LEVEL = 'Commentaar'

# Define (lowercased) levels that should not be cleaned
# Currently, only comment rows should be excempt
NO_CLEAN_LEVELS = (SAF_COMMENT_LEVEL.lower(), )
