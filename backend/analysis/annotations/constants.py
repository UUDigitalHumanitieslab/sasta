from typing import Counter, Dict, Optional, Tuple

from annotations.constants import (SAF_COMMENT_COLUMN, SAF_COMMENT_HEADERS, SAF_COMMENT_LEVEL, SAF_FASES_COLUMN,
                                   SAF_FASES_HEADERS, SAF_LEVEL_HEADER, SAF_LEVEL_HEADERS,
                                   SAF_SPEAKER_COLUMNS, SAF_SPEAKER_HEADER, SAF_UNALIGNED_LEVEL, SAF_UNALIGNED_LEVELS, SAF_UTT_HEADER, SAF_UTT_LEVELS)

# Type annotations
TupleStrDict = Dict[Tuple[Optional[str], Optional[str]], str]
CounterDict = Dict[str, Counter[str]]

# Global
ITEMSEPPATTERN = r'[,-; ]'
LABELSEP = ','

HEADER_VARIANTS = {
    SAF_UTT_HEADER.lower(): SAF_UTT_LEVELS,
    SAF_SPEAKER_HEADER.lower(): SAF_SPEAKER_COLUMNS,
    SAF_UNALIGNED_LEVEL.lower(): SAF_UNALIGNED_LEVELS,
    SAF_LEVEL_HEADER.lower(): SAF_LEVEL_HEADERS,
    SAF_FASES_COLUMN.lower(): SAF_FASES_HEADERS,
    SAF_COMMENT_COLUMN.lower(): SAF_COMMENT_HEADERS

}


PREFIX = ""
ALTITEMSEP = IMPLIESSEP = ','

# Define (lowercased) levels that should not be cleaned
# Currently, only comment rows should be excempt
NO_CLEAN_LEVELS = [*SAF_COMMENT_HEADERS]
