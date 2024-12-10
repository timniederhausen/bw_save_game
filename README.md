# bw_save_game: BioWare save game tools

This pure-Python library can read and write _Dragon Age: The Veilguard_ save files (`*.csav`).
It also comes with several tools (`csav2json`, `json2csav`) that can convert the save games to and from easily editable `.json` documents.

## Installation

Make sure you have these programs installed:

* Python 3.8 or newer

This package is available for download from [PyPI][1]. You can install it using `pip`:
```bash
pip install --upgrade bw_save_game
```

## Usage

For non-programmers this project ships two applications that can convert a save game into a human-readable JSON document and vice-versa.
Editing this document allows you to change every part of a save, however, ensuring correctness and consistency is up to you.

The following command converts `0-439591 Saria-Save 9 #874.csav` to JSON:
```bash
csav2json "0-439591 Saria-Save 9 #874.csav" my_wip_save.json
```
Converting the edited save file `my_wip_save.json` back to the game's binary save game format is as easy as running:
```bash
json2csav my_wip_save.json "0-439591 Saria-Save 9 #874-NEW.csav"
```

## Contributing

### Making Changes & Contributing

This project uses [pre-commit][4], please make sure to install it before making any
changes::

    pip install pre-commit
    cd bw_save_game
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

## Licensing

[![GNU GPLv3 Image](https://www.gnu.org/graphics/gplv3-127x51.png)][2]

`bw_save_game` is Free Software: You can use, study, share and improve it at your
will. Specifically you can redistribute and/or modify it under the terms of the
[GNU General Public License][3] as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

[1]: https://pypi.org/project/bw_save_game/
[2]: http://www.gnu.org/licenses/gpl-3.0.en.html
[3]: https://www.gnu.org/licenses/gpl.html
[4]: https://pre-commit.com/
