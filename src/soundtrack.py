import os


class SoundTrack:
    def __init__(self, path: str)->None:
        self.path = path
        self.file_name = os.path.basename(path)
        self.studio = os.path.basename(os.path.dirname(path))

    def __str__(self)->str:
        return f"Soundtrack: {self.file_name} from {self.studio}"