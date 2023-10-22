import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

from FileHelper import *


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
        f = FileHelper("liked.json")

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
                    name: {"artist": artist,
                           "id": track['id']}
                }
                obj.update(track_dict)
                print(obj)

        if f.exists():
            pre = json.loads(f.read())
            obj.update(pre)
        js = json.dumps(obj)
        f.overwrite(js)
