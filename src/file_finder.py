import glob
import os
import re
from typing import List


class FileFinder:
    video_extensions = ["*.mp4", "*.mkv", "*.avi", "*.flv", "*.webm", "*.mov"]

    def find_files(self, directory: str, template: str, recursive: bool) -> List[str]:
        search_pattern = os.path.join(directory, template)
        search_pattern = re.sub(r'\[', '[[]', search_pattern)
        search_pattern = re.sub(r'(?<!\[)\]', '[]]', search_pattern)
        return glob.glob(search_pattern, recursive=recursive)

    def find_videofiles(self, directory: str) -> List[str]:
        file_results = []
        for ext in self.video_extensions:
            file_results += self.find_files(directory, ext, recursive=False)

        return file_results
