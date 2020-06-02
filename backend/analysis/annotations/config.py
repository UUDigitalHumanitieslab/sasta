from typing import Counter, Dict, Tuple, Optional

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
