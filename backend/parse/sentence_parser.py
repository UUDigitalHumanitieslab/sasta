from django.conf import settings
from contextlib import contextmanager
import socket


class AlpinoSentenceParser:
    ''' Assumes a Alpino server is running on provided host:port,
    with assume_input_is_tokenized=off '''
    @contextmanager
    def connection(self):
        try:
            s = socket.create_connection(
                (settings.ALPINO_HOST, settings.ALPINO_PORT))
            yield s
            s.close()
        except socket.error:
            raise

    def parse_sentence(self, sentence: str, buffer_size=8096) -> str:
        with self.connection() as s:
            sentence += '\n\n'   # flag end of file
            s.sendall(sentence.encode('utf-8'))
            xml = b''
            while True:
                chunk = s.recv(buffer_size)
                if not chunk:
                    break
                xml += chunk
            return xml.decode('utf-8')
