import os
import re
from typing import List

from .file_finder import FileFinder
from .soundtrack import SoundTrack


class Episode:
    episode_pattern = re.compile(r"(\d+)")
    episode_pattern_blacklist = [
        "1080p",
        "720p",
        "480p",
        "x265",
        "x264",
    ]

    def __init__(self):
        # number is not used yet, but might be useful for custom episode naming like S01E01.mkv (plex loves that)
        self.number = 0
        self.file_name = ""
        self.path = ""
        self.soundtracks: List[SoundTrack] = []

    def __str__(self) -> str:
        result = f"Episode {self.number}: {self.file_name}"
        for soundtrack in self.soundtracks:
            result += f"\n\t{soundtrack}"

        return result

    def parse_videofile_path(self, file_path):
        self.path = file_path
        self.file_name = os.path.basename(file_path)
        name_no_ext = os.path.splitext(self.file_name)[0]
        for blacklist in self.episode_pattern_blacklist:
            name_no_ext = name_no_ext.replace(blacklist, "")

        match = self.episode_pattern.search(name_no_ext)
        if not match:
            raise ValueError(
                f"Could not parse episode number from file name: {self.file_name}"
            )

        for group in reversed(match.groups()):
            if group:
                self.number = int(group)
                break

        if self.number == 0:
            raise ValueError(
                f"Could not parse episode number from file name: {self.file_name}"
            )

    def scan_soundtracks(self, file_finder: FileFinder):
        host_dir = os.path.dirname(self.path)
        file_name_no_ext = os.path.splitext(self.file_name)[0]
        audio_paths = file_finder.find_files(
            host_dir, f"*Sound*/**/{file_name_no_ext}.*", recursive=True
        )
        if not audio_paths:
            raise ValueError(f"Could not find any audio files for {self.file_name}")

        for audio_path in audio_paths:
            self.soundtracks.append(SoundTrack(audio_path))
