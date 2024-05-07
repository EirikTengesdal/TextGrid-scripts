# TextGrid-scripts for Python
This repository contains Python scripts for generating and modifying [*Praat*](https://www.fon.hum.uva.nl/praat/) `TextGrid` files.

The most elaborate script is `TextGrid_script.py`, which is based on `CSVtoTextGrid.py`.

## About the main script `TextGrid_script.py`
[`TextGrid_script.py`](https://github.com/EirikTengesdal/TextGrid-script/blob/9f0d19e679d5abca6229ac721563ebf8401eecd8/TextGrid_script.py) is used in a project which involves using the online forced alignment app [*Autophon*](https://autophon.se/). The script is thus an example of how to operationalise project specific tasks.

This repository is made public in a preliminary state, and will be dynamic during the project period. Still, feel free to raise issues, create forks and/or make pull requests.

### Generating `TextGrid` files
The script enables the user to generate `TextGrid` files based on data contained within an input CSV file.
It also here presupposes that the corresponding audio files already are located within a folder, from which the audio file duration is extracted per file. This step can be replaced with other code for instance if the input CSV file already contains this information.

### Modifying `TextGrid` files
The script enables the user to modify pre-existing `TextGrid` files. It adds and/or manipulates `IntervalTier` and `PointTier` object variables.
It also features translation of `realization` labels in Norwegian into English via Google Translate (with `googletrans`: `Translator`).

## About the script `CSVtoTextGrid.py`
[`CSVtoTextGrid.py`](https://github.com/EirikTengesdal/TextGrid-script/blob/9f0d19e679d5abca6229ac721563ebf8401eecd8/CSVtoTextGrid.py) is the precursor to `TextGrid_script.py` and was originally used to generate TextGrids for longer audio files per participant.

(A related version of the script can be found in [my answer to a question on Stack Exchange about how to populate *Praat* TextGrid tiers based on another text file](https://linguistics.stackexchange.com/a/48642).)

An adapted version of this script can be relevant to use when you do not require to modify pre-existing TextGrids, or other more complex operations.

## Citation information
Please consider citing or acknowledging the repository/code if you have found it useful. For example like this:

Tengesdal, Eirik. 2024. TextGrid-script [Software]. https://github.com/EirikTengesdal/TextGrid-script

The repository was first published on GitHub 07.05.2024 (DD.MM.YYYY).

## Licence and copyright
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

© 2024 Eirik Tengesdal

Licensed under the [MIT License](LICENSE).

## Contact
Eirik Tengesdal<br />
Assistant Professor of Norwegian<br />
Department of Early Childhood Education (BLU)<br />
OsloMet – Oslo Metropolitan University<br />
eirik.tengesdal@oslomet.no

Guest Researcher of Linguistics<br />
Department of Linguistics and Scandinavian Studies (ILN)<br />
University of Oslo<br />
eirik.tengesdal@iln.uio.no

ORCID iD: [0000-0003-0599-8925](https://orcid.org/0000-0003-0599-8925)<br />
https://eiriktengesdal.no/
