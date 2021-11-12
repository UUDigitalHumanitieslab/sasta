from chamd.chat_reader import ChatHeader, ChatLine
from convert.chat_reader import ChatDocument
from typing import TextIO, Optional


class ChatWriter:
    def __init__(self, document, target=None, filename=None):
        self.document: ChatDocument = document
        self.filename: Optional[str] = filename
        self.target: TextIO = target or open(filename, 'w')
        self.all_entries = sorted(
            self.document.lines + self.document.headers,
            key=lambda x: self._get_lineno(x))

    @staticmethod
    def _get_lineno(el):
        if isinstance(el, ChatLine):
            return int(el.metadata['uttstartlineno'].text)
        elif isinstance(el, ChatHeader):
            return el.linestartno

    def write(self):
        for e in self.all_entries:
            if isinstance(e, ChatLine):
                self.write_line(e)
                for _, t in e.tiers.items():
                    self.write_tier(t)
            elif isinstance(e, ChatHeader):
                self.write_header(e)
        self.target.write('@End')
        if self.filename:
            self.target.close()

    def write_header(self, header):
        self.target.write(header.line+'\n')

    def write_line(self, line):
        spkr_code = line.metadata['speaker'].text
        text = line.original
        self.target.write(f'*{spkr_code}:\t{text}\n')

    def write_tier(self, tier):
        self.target.write(f'%{tier.id}:\t{tier.text}\n')
