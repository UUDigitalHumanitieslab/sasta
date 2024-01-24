from annotations.utils import preflabel
from sastadev.SAFreader import (commentsheaders, stagesheaders,
                                unalignedheaders, uttidheaders, levelheaders)

SAF_COMMENT_LEVEL = preflabel(commentsheaders, str.capitalize)
SAF_COMMENT_COLUMN = preflabel(commentsheaders, str.capitalize)

SAF_UTT_LEVEL = preflabel(uttidheaders, str.capitalize)
SAF_UNALIGNED_LEVEL = preflabel(unalignedheaders, str.capitalize)

SAF_LEVEL_HEADER = preflabel(levelheaders, str.capitalize)

SAF_FASES_COLUMN = preflabel(stagesheaders, str.capitalize)

# Composed headers
PRE_WORDS_HEADERS = ['ID', SAF_LEVEL_HEADER, SAF_UNALIGNED_LEVEL]
POST_WORDS_HEADERS = [SAF_FASES_COLUMN, SAF_COMMENT_COLUMN]

PRIMARY_COLOR = '3f51b5'
SECONDARY_COLOR = 'b5a33f'
