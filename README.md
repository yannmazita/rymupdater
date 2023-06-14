# rymupdater

**rymupdater** is an id3 tag updater using information found at rateyourmusic.com.
Work in progress.

## Dependencies

- chromium
- python >= 3.10
- mutagen = 1.46.0
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

## Todo
- GUI
- Credit tagging
- Release and recording time format standardisation
- Handling of eventual single releases in albums and EPs
- Binary package
