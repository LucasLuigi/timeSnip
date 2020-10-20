# timeSnip

## Overview

This script allows to update a text file with the music currently played from a one-video music mix (from Youtube or from a file for instance), by submitting an URL of a Youtube video mixes. Usually, its description contains a list of chapters following this format: "timecode Music name".
This project can be seen as a complement (or not) of Snip, and can be used for streamers to display music name.

## Features 

### Current (work in progress)

* Youtube URL is passed as argument and the script automatically parses the description field to get the chapters
* Parsed chapters list can follows different formats (pattern)
* If the parsed description contains to chapter list, the user has a second attempt to paste the chapter list if it is written in a commentary for example
* Format the output file text in a customized way (artist name, album, mix name, separation...)

### Evolutions

* Manually pause and play the time counting: manual synchronization between the output file text and the listened music
* Detect pause on Youtube video/media: automatic synchronization

## How to start

* Use python3
* Call these pip install:
```
pip install --upgrade google-api-python-client
pip install --upgrade google-auth-oauthlib google-auth-httplib2
```
* Add a JSON credential file _credentials/google-api-key.json coming from Google Developper Console. A project is needed and you will need to setup a OAuth 2.0 client ID. Visit the [Youtube API v3 documentation](https://developers.google.com/youtube/v3/getting-started) for further information.

```
I need more information on this file, maybe it can be pushed on Git... More news coming
```

* Run timeSnip:
```
python src\timeSnip.py
```