# timeSnip

## Overview

This script allows to update a text file with the music currently played from a one-video music mix (from Youtube or from a file for instance), by submitting an URL of a Youtube video mixes. Usually, its description contains a list of chapters following this format: "timecode Music name".
This project can be seen as a complement (or not) of Snip, and can be used for streamers to display music name.

## Features (work in progress)

* Youtube URL is passed as argument and the script automatically parses the description field to get the chapters
* Parsed chapters list can follows different formats (pattern)
* Format the output file text in a customized way (artist name, album, mix name, separation...)

## Evolutions

* Manually pause and play the time counting: manual synchronization between the output file text and the listened music
* Detect pause on Youtube video/media: automatic synchronization
