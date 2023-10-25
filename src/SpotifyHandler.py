import spotipy
import json
import re
from spotipy.oauth2 import SpotifyOAuth

from FileHelper import *
from DataManager import *


class SpotifyHandler:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = "user-library-read"

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=self.scope, client_id=self.client_id, client_secret=self.client_secret,
                                      redirect_uri="http://localhost:1908"))

    def get_liked_track(self, progress_callback):
        count = 0
        remain = True
        f = FileHelper("Liked tracks.json")

        obj = {}
        while remain:
            remain = False
            res = self.sp.current_user_saved_tracks(offset=count)
            for idx, item in enumerate(res['items']):
                remain = True
                count += 1
                progress_callback.emit(count)
                track = item['track']
                artist = ""
                for a in track["artists"]:
                    if a != track["artists"][0]:
                        artist += ", "
                    artist += a["name"]
                name = track['name']
                print(track, artist, name)

                track_dict = {
                    track["id"]: {
                        "name": name,
                        "artist": artist,
                        "album": track["album"]["name"],
                        "album-image-url": track["album"]["images"][0]["url"],
                        "source": "Spotify",
                    }
                }
                obj.update(track_dict)
                print(obj)

        js = json.dumps(obj)
        f.overwrite(js)

        dm = DataManager()
        dm.add_source("Liked tracks.json").update()

    def get_playlist_track(self, playlist_id, progress_callback):
        count = 0
        remain = True

        playlist_name = self.sp.playlist(playlist_id)["name"]
        playlist_name = re.sub('[\\/?:*"<>|]', '', playlist_name)
        if playlist_name in ["secrets", "data", "sources"]:
            playlist_name = playlist_name+"#"
        print(playlist_name)
        obj = {}
        while remain:
            remain = False
            res = self.sp.playlist_items(playlist_id, offset=count)
            for idx, item in enumerate(res['items']):
                remain = True
                count += 1
                progress_callback.emit(count)
                track = item['track']
                artist = ""
                for a in track["artists"]:
                    if a != track["artists"][0]:
                        artist += ", "
                    artist += a["name"]
                name = track['name']
                print(artist, name)

                track_dict = {
                    track["id"]: {
                        "name": name,
                        "artist": artist,
                        "album": track["album"]["name"],
                        "album-image-url": track["album"]["images"][0]["url"],
                        "source": "Spotify",
                    }
                }
                obj.update(track_dict)
                print(obj)
        f = FileHelper(playlist_name+".json")
        js = json.dumps(obj)
        f.overwrite(js)

        dm = DataManager()
        dm.add_source(playlist_name+".json").update()
