from typing import Dict, List, Optional, Set

from chamd.chat_reader import ChatFile, ChatHeader, ChatLine
from chamd.chat_reader import ChatReader as ChatParser
from chamd.chat_reader import MetaValue

TARGET_ROLES = ['Target_Child', 'Target_Adult', 'Participant']


class ChatDocument:
    def __init__(self, read_document: ChatFile):
        # TODO: get raw headers
        self.headers: Dict = read_document.headers or []
        self.file_metadata: Dict[str, MetaValue] = read_document.metadata or {}
        self.charmap: Dict[str, str] = read_document.charmap or {}
        self.lines: List[ChatLine] = read_document.lines or []
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
        participants = self.headers.get('participants')
        results |= self.find_target_roles(participants)
        ids = self.headers.get('id')
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
