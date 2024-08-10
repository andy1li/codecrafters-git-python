from git.object import Object


class Blob(Object):
    @staticmethod
    def from_file(filename: str) -> 'Blob':
        with open(filename, 'rb') as f:
            raw_bytes = f.read()
        return Blob(b'blob', len(raw_bytes), raw_bytes)
