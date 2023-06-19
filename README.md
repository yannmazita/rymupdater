# rymupdater

**rymupdater** is an id3 tag updater using information found at rateyourmusic.com.
Work in progress.

## Dependencies

- chromium
- python >= 3.10
- mutagen = 1.46.0
- jellyfish = 0.11.2
- selenium = 4.8.3
- webdriver-manager = 3.8.5

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
- Handling of different user locales when scrapping dates
- Handling of eventual single releases in albums and EPs
- Handling of sorting tags
- Use of ISO 639-2/B codes for the language tags
- Binary package
- (Vorbis)
