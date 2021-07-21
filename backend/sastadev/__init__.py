import logging
import os.path as op
from parse.sentence_parser import parse

SDLOGGER = logging.getLogger('sasta')  # logging object
SD_DIR = op.dirname(op.abspath(__file__))  # local directory

# Function to parse a sentence with Alpino
# Should take a string as input and return an lxml.etree
PARSE_FUNC = parse
