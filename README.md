# mass-mkvmerge

A simple app to merge all the mkv files in a directory into a single file.
It takes every video file in the directory and searches for corresponing audiotrack files in `*Sound*` subdirectory (recursive search used).
Expected file structure:
```
./workdir
├── file1.mkv
├── file2.mkv
├── file3.mkv
├── Sound
|   |-- studio1
│   ├   |── file1.mka
│   ├   |── file2.mka
│   ├   |── file3.mka
|   |-- studio2
│   ├   |── file1.mka
│   ├   |── file2.mka
│   ├   |── file3.mka
```
`file1_merged.mkv`, `file2_merged.mkv`, `file3_merged.mkv` will be created in the same directory as the original files.
Each merged file will contain all the audio tracks from the corresponding `Sound` subdirectory. `studio1` and `studio2` will be used as audiotrack name.

## Usage
Restore the dependencies:
```bash 
pip install -r requirements.txt
```

Run the app:
```bash
usage: app.py [-h] [--dry-run] [--verbose] [--delete-source-files] directory

positional arguments:
  directory             Directory to search for files. Current directory by default.

options:
  -h, --help            show this help message and exit
  --dry-run
  --verbose
  --delete-source-files
```