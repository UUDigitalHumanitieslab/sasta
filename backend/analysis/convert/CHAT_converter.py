import errno
import os
import re

AGE_FIELD_NAMES = ['age', 'leeftijd']
SEX_FIELD_NAMES = ['sex', 'gender', 'geslacht']
MALE_CODES = ['jongen', 'man', 'boy', 'man']
FEMALE_CODES = ['meisje', 'vrouw', 'girl', 'woman']


class CHATConverter:
    def __init__(self, file, outfile):
        self.input_path = file
        self.output_path = outfile

        self.transcript_header = '@UTF-8\n@Begin\n@Languages:\tnld\n'
        self.transcript_content = ''
        self.transcript_footer = '@End'
        self.metadata = []
        self.metadata_coms = '\n'
        self.participants = []
        self.ids = ''

        # TODO multiple target speakers
        self.target_speaker = {'code': None, 'age': '',
                               'sex': '', 'role': 'Target_Adult'}

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

        return [re.compile(p) for p in [
            meta_pattern, utterance_pattern,
            tier_pattern, single_speaker_pattern,
            target_uttids_pattern]]

    def read(self):
        with open(self.input_path, 'r') as file:
            for line in file.readlines():
                [meta, utt, tier, single_spk, _tar_uttids] = [self.match_pattern(
                    pattern, line) for pattern in self.patterns]
                if meta:
                    dtype, field, value = meta
                    self.metadata.append({'dtype': dtype,
                                          'field': field, 'value': value})
                elif utt:
                    self.parse_utt(utt)
                elif tier:
                    self.transcript_content += line
                elif single_spk:
                    self.target_speaker['code'] = single_spk[0]
                else:
                    pass

        self.parse()
        self.write()

    def parse(self):
        meta = self.parse_metadata()
        self.make_participant_ids(self.target_speaker, self.participants)
        if meta:
            self.transcript_header += f'\n{"".join(meta)}\n'

        print(self.transcript_header)
        print(self.transcript_content)
        print(self.transcript_footer)

    def write(self):
        output_dir = os.path.dirname(self.output_path)
        try:
            os.makedirs(output_dir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(output_dir):
                pass
            else:
                raise

        with open(self.output_path, 'w', encoding='utf-8') as file:
            file.write(self.transcript_header)
            file.write(self.transcript_content)
            file.write(self.transcript_footer)

    def match_pattern(self, pattern, line):
        match = re.match(pattern, line)
        if not match:
            return None
        else:
            return match.groups()

    def parse_utt(self, utterance):
        u_id, spk, utt = utterance
        if spk not in self.participants:
            self.participants.append(spk)
        out = f'*{spk}:\t{utt}\n'
        if u_id:
            out += f'%xuid:\t{u_id}\n'
        self.transcript_content += out

    def parse_metadata(self):
        # groups:   1) years    2) months   3) days
        age_pattern = re.compile(r'(\d+);(\d{2})?(?:(?:\.)(\d{2}))?')
        metadata_coms = []
        for meta in self.metadata:
            field_type, field, value = meta['dtype'], meta['field'], meta['value']

            if field.lower() in AGE_FIELD_NAMES:
                self.target_speaker['age'] = value
                years = int(age_pattern.match(value).group(1))
                self.target_speaker['role'] = 'Target_Child' if years < 18 else 'Target_Adult'

            elif field.lower() in SEX_FIELD_NAMES:
                if value.lower() in MALE_CODES:
                    self.target_speaker['sex'] = 'male'
                elif value.lower() in FEMALE_CODES:
                    self.target_speaker['sex'] = 'female'
                else:
                    self.target_speaker['sex'] = 'unknown'

            else:
                metadata_coms += f'@Comment ##META {field_type} {field} = {value}'

        return metadata_coms

    def make_participant_ids(self, tar_speaker, other_speakers):
        # TODO implement name/role translations for commonly used speaker codes
        speakers = [
            f'{tar_speaker["code"]} {tar_speaker["code"].lower()} {tar_speaker["role"]}']
        for code in [spk for spk in other_speakers if spk != tar_speaker['code']]:
            speakers.append(f'{code} {code.lower()} Other')

        participants_header = f'@Participants:\t{", ".join(speakers)}\n'

        target_speaker_id = f'@ID:\tnld||{tar_speaker["code"]}|{self.target_speaker["age"]}|{tar_speaker["sex"]}|||{tar_speaker["role"]}|||\n'
        participant_ids = [f'@ID:\tnld||{code}|||||Other|||\n' for code in [
            p for p in other_speakers if p != tar_speaker['code']]]

        self.transcript_header += participants_header
        self.transcript_header += target_speaker_id
        self.transcript_header += ''.join(participant_ids)
