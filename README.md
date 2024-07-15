# rymupdater
rymupdater is now read only. RYM has made scrapping somewhat more difficult without offering an API.

**rymupdater** is an id3 tag updater using information found at rateyourmusic.com.
Work in progress.

## Dependencies

- chromium
- python = 3.11
- mutagen = 1.46.0
- jellyfish = 0.11.2
- selenium = 4.12.0
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

Inside the cloned repository:
```commandline
python -m src.presentation.app
```
The GUI will start by default when no arguments are provided.

### CLI

To start the CLI:
```commandline
python -m rymupdater.presentation.app -c "/path/of/music/directory"
```
Use full paths.

### GUI

To explicitly start the GUI:
```commandline
python -m rymupdater.presentation.app -g
```

## Todo
- Credit tagging
- Handling of eventual single releases in albums and EPs
- Binary package
- (Vorbis)
