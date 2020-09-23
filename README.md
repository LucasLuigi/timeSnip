# timeSnip

## Overview

This script allows to update a text file with the music currently played from a one-video music mix (from Youtube or from a file for instance), by submitting a text containing a list of "timecode - music name", usually found in Youtube video mixes' descriptions.
This project can be seen as a complement (or not) of Snip, and can be used for streamers to display music name.

## Features (work in progress)

* Accept timecodes list in standard input following different formats
* Start, pause and reset timer for manual synchronization between the output file text and the listened music
* Format the output file text in a customized way (artist name, album, mix name, separation...)

## Evolutions

* Detect pause on Youtube video/media: automatic synchronization
* Automatic detection of the Youtube mix song listened and automatic parsing of the description field
