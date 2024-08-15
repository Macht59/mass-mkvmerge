import os
import sys
from unittest import TestCase
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.file_finder import FileFinder
from src.episode import Episode


class EpisodeTests(TestCase):

    def setUp(self):
        pass

    def test_parse_videofile_path(self):
        test_cases = [
            ("/path/to/series/video1.mp4", 1, "video1.mp4"),
            (
                "/path/[AniDub]_Kubikiri_Cycle_-_Aoiro_Savant_to_Zaregototsukai_[07]_[BDRip_1920x1080_x264_Aac]_[MVO].mp4",
                7,
                "[AniDub]_Kubikiri_Cycle_-_Aoiro_Savant_to_Zaregototsukai_[07]_[BDRip_1920x1080_x264_Aac]_[MVO].mp4",
            ),
        ]
        for file_path, expected_number, expected_file_name in test_cases:
            with self.subTest(file_path=file_path):
                episode = Episode()
                episode.parse_videofile_path(file_path)
                self.assertEqual(episode.number, expected_number)
                self.assertEqual(episode.file_name, expected_file_name)
                self.assertEqual(episode.path, file_path)

    def test_scan_soundtracks(self):
        # Arrange
        video_path = "/path/to/series/ep15.mp4"
        audio_track1 = "/path/to/series/Sound/lostfilm/ep15.mp3"
        audio_track2 = "/path/to/series/Sound/hdrezka/ep15.aac"
        audio_track3 = "/path/to/series/Sound/kubik/ep15.mka"

        file_finder: FileFinder = MagicMock(
            find_files=MagicMock(
                return_value=[audio_track1, audio_track2, audio_track3]
            )
        )

        # Act
        episode = Episode()
        episode.parse_videofile_path(video_path)
        episode.scan_soundtracks(file_finder)

        # Assert
        self.assertEqual(len(episode.soundtracks), 3)
        self.assertEqual(episode.soundtracks[0].path, audio_track1)
        self.assertEqual(episode.soundtracks[0].studio, "lostfilm")
        self.assertEqual(episode.soundtracks[1].path, audio_track2)
        self.assertEqual(episode.soundtracks[1].studio, "hdrezka")
        self.assertEqual(episode.soundtracks[2].path, audio_track3)
        self.assertEqual(episode.soundtracks[2].studio, "kubik")
