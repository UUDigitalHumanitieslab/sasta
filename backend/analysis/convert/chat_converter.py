import errno
import os
import re
from typing import List, Optional, Union, Pattern

# TODO handle corpus name/transcript title
# TODO move to config
AGE_FIELD_NAMES = ['age', 'leeftijd']
SEX_FIELD_NAMES = ['sex', 'gender', 'geslacht']
TITLE_FIELD_NAMES = ['samplename', 'title', 'titel']
MALE_CODES = ['jongen', 'man', 'boy', 'man']
FEMALE_CODES = ['meisje', 'vrouw', 'girl', 'woman']


def match_pattern(pattern: Pattern, line: str):
    match = re.match(pattern, line)
    if not match:
        return None
    if match and match.groups():
        return match.groups()
    return match


class Participant:
    def __init__(self, code: str,
                 age: Optional[str] = None, sex: Optional[str] = None,
                 role: Optional[str] = None, target_speaker=False):
        self.code = code
        self.age = age
        self.sex = sex
        self.role = role
        self.target_speaker = target_speaker

    def role_from_age(self) -> str:
        '''returns a role based on age (if present)'''
        age_pattern = re.compile(r'(\d+);(\d{2})?(?:(?:\.)(\d{2}))?')

        if self.age:
            match = age_pattern.match(self.age)
            if match:
                years = int(match.group(1))
                return 'Target_Child' if years < 18 else 'Target_Adult'
        return 'Other'

    @property
    def id_header(self) -> str:
        '''CHAT @ID header'''
        return f'@ID:\tnld||{self.code}|{self.age or ""}|{self.sex or ""}|||{self.role or self.role_from_age()}|||'

    @property
    def participant_header(self) -> str:
        '''part of CHAT @Participants header'''
        return f'{self.code} {self.code.lower()} {self.role or self.role_from_age()}'


class Utterance:
    def __init__(self, speaker_code: str, text: str, utt_id: Optional[int] = None):
        self.speaker_code = speaker_code
        self.utt_id = utt_id
        self.text = text

    def __str__(self):
        return f'*{self.speaker_code}:\t{self.text}' + ('\n'+str(Tier('xsid', self.utt_id)) if self.utt_id else '')


class Tier:
    def __init__(self, code: str, value: str):
        self.code = code
        self.value = value

    def __str__(self):
        return f'%{self.code}:\t{self.value}'


class MetaValue:
    def __init__(self, field_type: str, key: str, value: Union[str, int]):
        self.field_type = field_type
        self.key = key
        self.value = value.strip() if isinstance(value, str) else value


class MetaComment(MetaValue):
    '''Metadata that is copied as a comment to the CHAT format'''

    def __str__(self):
        return f'@Comment:\t##META {self.field_type} {self.key} = {self.value}'


class SifDocument:
    def __init__(self,
                 participants: List[Participant],
                 content: List[Union[Utterance, Tier]],
                 meta_comments: List[MetaComment]):
        self.participants = participants
        self.content = content
        self.meta_comments = meta_comments

    def write_chat(self, out_file_path: str):
        output_dir = os.path.dirname(out_file_path)
        try:
            os.makedirs(output_dir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(output_dir):
                pass
            else:
                raise

        with open(out_file_path, 'w', encoding='utf-8') as file:
            # File headers
            print('@UTF8', '@Begin', '@Languages:\tnld', sep='\n', file=file)
            # @Participants header
            print(
                f'@Participants:\t{", ".join([p.participant_header for p in self.participants])}', file=file)
            # @ID headers
            print(*[p.id_header for p in self.participants], sep='\n', file=file)
            # Metadata comments
            print(*self.meta_comments, sep='\n', file=file)
            print('\r', file=file)
            # Content (utterances and tiers)
            print(*self.content, sep='\n', file=file)
            # Footer
            print('@End', file=file)


class SifReader:
    def __init__(self, in_file_path: str):
        self.file_path = in_file_path

        self.participants: List[Participant] = []
        self.content: List[Union[Utterance, Tier]] = []
        self.metadata: List[MetaValue] = []
        self.meta_comments: List[MetaComment] = []

        self.read()
        self.parse_metadata()

    @property
    def document(self):
        return SifDocument(self.participants, self.content, self.meta_comments)

    @property
    def patterns(self):
        # groups:   1) type     2) field    3) value
        meta_pattern = r'^##META\s+(\w+)\s+(\w+)\s=\s(.*)$'
        # groups:   1) optional utterance_id    2) speaker code     3) utterance
        utterance_pattern = r'^(?:(\S+)\s*\|.*?)?\*?([A-Z*]{3}):(?:\s*)(.*)$'
        # groups:   1) utterance_id     2) speaker code     3) utterance
        utterance_with_id_pattern = r'^(?:(\S+)\s*\|.*?)\*?([A-Z*]{3}):(?:\s*)(.*)$'
        # groups:   1) tier code    2) value
        tier_pattern = r'^(%\w{3,4}):\s*(.*)$'
        # groups:   1) speaker code
        single_speaker_pattern = r'^##TARGET\sSPEAKER(?:S)?\s=\s([A-Z]{3})$'
        # no groups
        target_uttids_pattern = r'^##TARGET\sUTTIDS$'

        return [re.compile(p) for p in [
            meta_pattern, utterance_pattern,
            tier_pattern, single_speaker_pattern,
            target_uttids_pattern, utterance_with_id_pattern]]

    def parse_utterance(self, utterance):
        utt_id, code, text = utterance
        known_participant_codes = [p.code for p in self.participants]
        if code not in known_participant_codes:
            self.participants.append(Participant(code))

        self.content.append(Utterance(code, text, utt_id))

    def parse_metadata(self):
        ''' Metadata pertaining to target speaker'''
        target_speaker = [
            p for p in self.participants if p.target_speaker][0] or None
        for meta in self.metadata:
            # parse age
            if meta.key.lower() in AGE_FIELD_NAMES:
                target_speaker.age = meta.value
            # parse sex
            elif meta.key.lower() in SEX_FIELD_NAMES:
                if meta.value.lower() in MALE_CODES:
                    target_speaker.sex = 'male'
                elif meta.value.lower() in FEMALE_CODES:
                    target_speaker.sex = 'female'
                else:
                    target_speaker.sex = 'unknown'

    def read(self):
        with open(self.file_path, 'r') as file:
            file_lines = file.readlines()
            for line in list(file_lines):
                [meta, utt, tier, single_spk, tar_uttids, _utt_w_id] = [match_pattern(
                    pattern, line) for pattern in self.patterns]
                if meta:
                    if meta[1] in AGE_FIELD_NAMES or meta[1] in SEX_FIELD_NAMES:
                        self.metadata.append(
                            MetaValue(*meta))
                    else:
                        self.meta_comments.append(MetaComment(*meta))
                elif utt:
                    self.parse_utterance(utt)
                elif tier:
                    self.content.append(Tier(*tier))
                elif single_spk:
                    self.participants.append(Participant(
                        *single_spk, target_speaker=True))
                elif tar_uttids:
                    for line in list(file_lines):
                        find_utt = re.match(
                            r'^\S+\s*\|.*?\*?([A-Z*]{3}):\s*.*$', line)
                        if find_utt:
                            self.participants.append(Participant(
                                *find_utt.groups(), target_speaker=True))
                            break
