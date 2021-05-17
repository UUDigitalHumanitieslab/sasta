from typing import Dict, List, Optional, Set

from chamd.chat_reader import ChatFile, ChatHeader, ChatLine
from chamd.chat_reader import ChatReader as ChatParser
from chamd.chat_reader import MetaValue

TARGET_ROLES = ['Target_Child', 'Target_Adult', 'Participant']


class ChatDocument:
    def __init__(self, inputdoc: ChatFile):
        self.headers: List[ChatHeader] = inputdoc.headers or []
        self.header_metadata: Dict = inputdoc.header_metadata or {}
        self.file_metadata: Dict[str, MetaValue] = inputdoc.metadata or {}
        self.charmap: Dict[str, str] = inputdoc.charmap or {}
        self.lines: List[ChatLine] = inputdoc.lines or []
        # SASTA specific attributes
        self.target_speakers: Set[str] = self.find_target_speakers()
        self.target_uttids: bool = self.has_xsids

    @classmethod
    def from_chatfile(cls, filepath: str):
        reader = ChatParser()
        doc = reader.read_file(filepath)
        # TODO: probably want to let this condition go if it
        # only concerns warning
        assert not reader.errors
        return cls(doc)

    def find_target_speakers(self):
        results = set([])
        participants = self.header_metadata.get('participants')
        results |= self.find_target_roles(participants)
        ids = self.header_metadata.get('id')
        results |= self.find_target_roles(ids)
        return results

    @staticmethod
    def find_target_roles(header: Optional[Dict]) -> Set[str]:
        if not header:
            return set([])
        return {
            code for (code, info) in header.items()
            if info['role'] in TARGET_ROLES
        }

    @property
    def has_xsids(self) -> bool:
        tiers = [ln.tiers for ln in self.lines]
        return any(t.get('xsid') for t in tiers)

    def __eq__(self, other):
        safe_headers = ('session',)
        if ([h.__dict__ for h in self.headers] !=
                [h.__dict__ for h in other.headers]):
            return False

        if self.header_metadata.keys() != other.header_metadata.keys():
            return False
        for k, v in self.header_metadata.items():
            if other.header_metadata[k] != v:
                if k not in safe_headers:
                    return False

        if self.file_metadata.keys() != other.file_metadata.keys():
            return False
        for k, v in self.file_metadata.items():
            if str(v) != str(other.file_metadata[k]):
                if k not in safe_headers:
                    return False

        if self.charmap != other.charmap:
            return False

        for i, ln in enumerate(self.lines):
            otherln = other.lines[i]
            if ln.original != otherln.original:
                return False
            if [str(t) for t in ln.tiers] != [str(t) for t in otherln.tiers]:
                return False

        return True
