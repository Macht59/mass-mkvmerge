import logging
import argparse
import os
from pymkv import MKVFile, MKVTrack

from src.episode import Episode
from src.file_finder import FileFinder


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Merges multiple video tracks with corresponding audio tracks in a directory if namesa are similar"
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Directory to search for files. Current directory by default.",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
    )
    parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
    )
    parser.add_argument(
        "--delete-source-files",
        dest="delete_source_files",
        action="store_true",
    )
    parser.add_argument(
        "--episode-from",
        type=int,
        dest="episode_from",
        default=1,
    )
    parser.add_argument(
        "--episode-to",
        type=int,
        dest="episode_to",
        default=9999,
    )
    args = parser.parse_args()

    directory = args.directory
    logging.info(f"Searching for files in {directory}")

    file_finder = FileFinder()
    ep_paths = file_finder.find_videofiles(directory)

    if not ep_paths:
        logging.warning(f"No video files found in {directory}")
        return

    for ep_path in ep_paths:
        ep = Episode()
        ep.parse_videofile_path(ep_path)
        ep.scan_soundtracks(file_finder)
        if args.verbose:
            logging.info(ep)
        if args.episode_from <= ep.number <= args.episode_to:
            if args.verbose:
                logging.info(f"Episode is in range")
        else:
            if args.verbose:
                logging.info(f"Skipping out of range episode")
            continue
        if not args.dry_run:
            mkv = MKVFile(ep.path)
            for soundtrack in ep.soundtracks:
                track = MKVTrack(soundtrack.path)
                track.language = "rus"
                track.track_name = soundtrack.studio
                mkv.add_track(track)
            
            new_name = ep_path.replace(".mkv", "_merged.mkv")
            logging.info(f"Writing {new_name}")
            mkv.mux(new_name)
            logging.info(f"Done")
            if args.delete_source_files:
                logging.info(f"Deleting {ep.path}")
                os.remove(ep.path)
                for soundtrack in ep.soundtracks:
                    logging.info(f"Deleting {soundtrack.path}")
                    os.remove(soundtrack.path)


if __name__ == "__main__":
    main()
