# -*-coding:Latin-1 -*

import os
import re

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from logPrint import *


class youtubeApiWrapper():

    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    videoId = "DEFAULT-VALUE"

    def __init__(self, youtubeUrl):
        logPrint.printLog("Initializing youtubeApiWrapper with "+youtubeUrl)
        logPrint.printDebug("youtubeUrl: "+youtubeUrl)
        self.videoId = self.extractIdFromUrl(youtubeUrl)

    # Extract the video ID from the Youtube URL
    def extractIdFromUrl(self, youtubeUrl):
        splittedListFromUrl = re.split(
            r'[^A-Za-z0-9\-]+', youtubeUrl)
        logPrint.printDebug("splittedListFromUrl: "+str(splittedListFromUrl))
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
        logPrint.printDebug("videoId: "+videoId)
        return videoId

    # Call the Youtube v3 API to get its description field
    def getDescriptionField(self):
        logPrint.printLog(
            "Calling Youtube API to get the video description list")

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # This file is secret
        # FIXME Authorize the case where the cwd is src and not its parent
        client_secrets_file = os.getcwd()+"\\_credentials\\google-api-key.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, self.scopes)
        # Calls OAUTH2 services on a Browser
        # FIXME Store credentials to prevent a new authorization at every run
        # credentials = flow.run_console()
        credentials = flow.run_local_server(
            success_message="Abonnez vous a LukkoLuigi sur Twitch")
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.videos().list(
            part="snippet",
            id=self.videoId
        )
        response = request.execute()
        #description = response.items[0].snippet.description
        items = response["items"]
        snippet = items[0]["snippet"]
        description = snippet["description"]

        # logPrint.printDebug("description: ")
        # logPrint.printDebug(description)

        return description


# Raised when the Youtube IRL is badly formatted
class urlBadlyFormatted(Exception):
    def __init__(self, message):
        self.message = "Error: "+message+". Exiting."
        logPrint.printError(message)
        exit(-2)
