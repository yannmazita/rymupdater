# rymupdater

**rymupdater** is an id3 tag updater using information found at rateyourmusic.com.
Work in progress.

## Dependencies

- chromium
- python >= 3.10
- mutagen = 1.47.0
- jellyfish = 0.11.2
- selenium = 4.12.0
- webdriver-manager = 3.9.1
- arrow = 1.2.3

## Installation

### Using Poetry

Inside the cloned repository:
```commandline
poetry install
```
### Using requirements.txt

Dependencies defined in requirements.txt can be installed in a virtual environment.
```commandline
python -m pip install -r requirements.txt
```
## Running

Inside the cloned repository
```commandline
python -m src.presentation.app "/path/of/music/directory"
```
Use full paths.

## Todo
- GUI
- Credit tagging
- Handling of eventual single releases in albums and EPs
- Binary package
- (Vorbis)
