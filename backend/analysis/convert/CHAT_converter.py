from ..models import File
import os
import errno
import re


class CHATConverter:
    def __init__(self, file):
        self.input_path = file.content.name
        self.dir_path = os.path.dirname(file.content.name)
        self.out_path = re.sub('\/uploads\/', '/converted/', self.dir_path)
        self.out_filename = os.path.join(
            self.out_path, os.path.basename(self.input_path)).replace('.txt', '.cha')

        self.transcript_header = '@UTF-8\n@Begin\n@Languages nld\n'
        self.transcript_content = '\n'
        self.metadata = {}
        self.participants = []
        self.ids = ''

    @property
    def patterns(self):
        # groups:   1) type     2) field    3) value
        meta_pattern = r'^##META\s+(\w+)\s+(\w+)\s=\s(.*)$'
        # groups:   1) optional utterance_id    2) speaker code     3) utterance
        utterance_pattern = r'^(?:(\S+)\s*\|.*?)?\*?([A-Z*]{3}):(?:\s*)(.*)$'
        # groups:   1) tier code    2) value
        tier_pattern = r'^(%\w{3,4}):\s*(.*)$'
        # groups:   1) speaker code
        single_speaker_pattern = r'^##TARGET\sSPEAKERS\s=\s([A-Z]{3})$'
        # no groups
        target_uttids_pattern = r'^##TARGET\sUTTIDS$'

        return [re.compile(p) for p in [meta_pattern, utterance_pattern, tier_pattern, single_speaker_pattern, target_uttids_pattern]]

    def read(self):
        with open(self.input_path, 'r') as f:
            for line in f.readlines():
                [meta, utt, tier, single_spk, tar_uttids] = [self.match_pattern(
                    p, line) for p in self.patterns]
                if meta:
                    pass
                elif utt:
                    self.parse_utt(utt)
                elif tier:
                    self.transcript_content += line
                # elif single_spk:
                #     print(self.target_speaker_id('CHI', '6;9'))
                else:
                    pass
        participants = [f'{p} NAME ROLE ' for p in self.participants]
        self.transcript_header += f'@Participants {", ".join(participants)}\n'
        self.transcript_header += self.ids
        self.write()

    def write(self):
        try:
            os.makedirs(self.out_path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(self.out_path):
                pass
            else:
                raise

        with open(self.out_filename, 'w') as f:
            f.write(self.transcript_header)
            f.write(self.transcript_content)
            f.write('@End\r')

    def match_pattern(self, pattern, line):
        m = re.match(pattern, line)
        if not m:
            return None
        else:
            return m.groups()

    def parse_utt(self, utterance):
        u_id, spk, utt = utterance
        if spk not in self.participants:
            self.participants.append(spk)
            self.target_speaker_id(spk, '')
        out = f'*{spk}:\t{utt}\n'
        if u_id:
            out += f'%xuid:\t{u_id}\n'
        self.transcript_content += out

    def target_speaker_id(self, code, age):
        # @ID: language|corpus|code|age|sex|group|SES|role|education|custom|
        info = {
            'language': 'nld',
            'corpus': '',
            'code': code,
            'age': age,
            'sex': '',
            'group': '',
            'SES': '',
            'role': '',
            'education': '',
            'custom': ''
        }

        self.ids += f'@ID {"|".join(info.values())}|\n'
