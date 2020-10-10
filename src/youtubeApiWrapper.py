# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import re

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from logPrint import *


class youtubeApiWrapper():

    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    videoId = "DEFAULT_VALUE"

    def __init__(self, youtubeUrl):
        print("Initializing youtubeApiWrapper with "+youtubeUrl)
        logPrint.printDebug("youtubeUrl = "+youtubeUrl)
        self.videoId = self.extractIdFromUrl(youtubeUrl)

    def extractIdFromUrl(self, youtubeUrl):
        splittedListFromUrl = re.split(
            r'[^A-Za-z0-9]+', youtubeUrl)
        logPrint.printDebug(splittedListFromUrl)
        # Expected format: ['http(s)', 'www', 'youtube', 'com', 'watch', 'v', '<ID>' ...]
        if (len(splittedListFromUrl) < 2):
            raise urlBadlyFormatted(
                "Url "+youtubeUrl+" badly formatted: too short")
        else:
            if (splittedListFromUrl[1] == "www"):
                # In the next robustness, count "www" as part of the list
                urlContainsWww = 1
            else:
                urlContainsWww = 0

        # Cf expected format
        if (len(splittedListFromUrl) < 7+urlContainsWww):
            raise urlBadlyFormatted(
                "Url "+youtubeUrl+" badly formatted: not enough parts")
        else:
            # Check if first word is http(s)
            if (not (splittedListFromUrl[0] == "http") and not (splittedListFromUrl[0] == "https")):
                raise urlBadlyFormatted(
                    "Url "+youtubeUrl+" badly formatted: not an URL")
            # Check if we are on Youtube
            if (not (splittedListFromUrl[1+urlContainsWww] == "youtube")):
                raise urlBadlyFormatted(
                    "Url "+youtubeUrl+" badly formatted: not a Youtube IRL")
            # Check if we are on a Youtube video (watch?v=)
            if (not (splittedListFromUrl[3+urlContainsWww] == "watch") or not (splittedListFromUrl[4+urlContainsWww] == "v")):
                raise urlBadlyFormatted(
                    "Url "+youtubeUrl+" badly formatted: not a Youtube video IRL")

        videoId = splittedListFromUrl[5+urlContainsWww]
        logPrint.printDebug("videoId = "+videoId)
        return videoId

    def getDescriptionField(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # This file is secret
        client_secrets_file = os.getcwd()+"\\_credentials\\google-api-key.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, self.scopes)
        # Calls OAUTH2 services on a Browser
        # FIXME Store credentials to prevent a new authorization at every run
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.videos().list(
            part="snippet",
            id=self.videoId
        )
        response = request.execute()

        print(response)


class urlBadlyFormatted(Exception):
    """Raised when the Youtube IRL is badly formatted
    """

    def __init__(self, message):
        self.message = "Error: "+message
        logPrint.printError(message)
        exit
