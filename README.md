# :musical_note: lrc-dl

An ultimate CLI tool for downloading lyrics for songs, inspired by other awesome *-dl projects.

## Installation

Before you begin, make sure you have `python3` and `pip` installed.

0. If you wish to use the `youtube` provider, install `ffmpeg` and add it to your `PATH`.
1. Clone the repository:
   ```bash
   git clone https://github.com/mrsobakin/lrc-dl.git
   ```
2. Navigate to the project directory:
   ```bash
   cd lrc-dl
   ```
3. Install the package:
   ```bash
   pip install .
   ```

## Usage

You can use `lrc-dl` both as a CLI tool and as a Python module.

### CLI Usage

```bash
lrc-dl [-h] [-c CONFIG] [-e EXTENSIONS] [-f] path
```

#### Positional Arguments:

- `path`: Path to the song file or directory

#### Options:

- `-h, --help`: Display help message and exit.
- `-c CONFIG, --config CONFIG`: Specify a custom config file (in TOML format) for `lrc-dl`.
- `-e EXTENSIONS, --extensions EXTENSIONS`: Define music file extensions, separated by commas (e.g., wav,flac,mp3).
- `-f, --force-override`: Force override .lrc file, if it already exists.

### Usage as a Python Module

You can also use `lrc-dl` as a Python module, allowing you to integrate its functionality directly into your own scripts or applications.

#### Initializing `LyricsDl`

```python
from lrc_dl import LyricsDl, LyricsDlConfig

# Create a LyricsDl instance with default configuration
ldl = LyricsDl()

# Create a LyricsDl instance with a custom configuration
config = LyricsDlConfig(order=["kugou"])
ldl = LyricsDl(config=config)
```

#### Fetching Lyrics for a Song

```python
from lrc_dl import Song

# Create a Song object
song = Song(title="Where'd All The Time Go?", artist="Dr. Dog")

# Fetch lyrics for the song
lyrics = ldl.fetch_lyrics(song)

if lyrics:
    print(lyrics)
else:
    print("Lyrics not found")
```

#### Processing a File

```python
from pathlib import Path

# Define the path to the song file
file_path = Path("/path/to/song.mp3")

# Process the file
ldl.process_file(file_path)
```

#### Processing a Directory

```python
from pathlib import Path

# Define the path to the directory
dir_path = Path("/path/to/songs/directory")

# Define the extensions of music files
extensions = ["mp3", "wav"]

# Process the directory
ldl.process_directory(dir_path, extensions)
```

For more detailed information on the usage of the `LyricsDl` class, `Song` class, and `LyricsDlConfig` class, you can explore the source code. The code is written with Python typing, making it easy to understand.

## Configuration

By default, lrc-dl searches for the configuration file at `$XDG_CONFIG_HOME/lrc-dl/config.toml`. You can specify custom config location using `-c` flag.

The configuration is using the TOML format.
Global provider parameters (for example, services order) are defined under the `[providers]` section.
To change provider-specific configuration, add a `[providers.provider_name]` section and set the required parameters under it.

As an example, to enable the `musixmatch` provider, you'll need to [acquire a Musixmatch token](https://web.archive.org/web/20230831151006/https://spicetify.app/docs/faq/#sometimes-popup-lyrics-andor-lyrics-plus-seem-to-not-work) and create a config like this:

```toml
[providers]
order = ["musixmatch", "kugou"]
delay = 10  # Seconds to wait between searches
prepend_header = true  # Prepend lrc-dl's & provider's header to keep track of lyrics source

[providers.musixmatch]
token = "YOUR_TOKEN"
```
