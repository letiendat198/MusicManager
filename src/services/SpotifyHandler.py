import spotipy
import re
import logging
from spotipy.oauth2 import SpotifyOAuth
from src.utils.DatabaseHelper import DatabaseHelper

logger = logging.getLogger(__name__)
class SpotifyHandler:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = "user-library-read"

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=self.scope, client_id=self.client_id, client_secret=self.client_secret,
                                      redirect_uri="http://localhost:1908"))

    def get_liked_track(self, progress_callback=None):
        count = 0
        remain = True

        tracks = {}
        while remain:
            remain = False
            res = self.sp.current_user_saved_tracks(offset=count)
            for idx, item in enumerate(res['items']):
                remain = True
                count += 1
                progress_callback.emit(count)
                track = item['track']
                album_artist = ", ".join([artist["name"] for artist in track["album"]["artists"]])
                artists = ", ".join([artist["name"] for artist in track["artists"]])
                track_number = track["track_number"]
                name = track['name']

                track_dict = {
                    track["id"]: {
                        "name": name,
                        "artist": artists,
                        "album": track["album"]["name"],
                        "album_artist": album_artist,
                        "track_number": track_number,
                        "album-image-url": track["album"]["images"][0]["url"],
                        "source": "Spotify",
                    }
                }
                tracks.update(track_dict)
            break

        db = DatabaseHelper()
        db.init_database()
        for id in tracks:
            if len(db.filter_row("playlists", "name", "Liked Songs").get_output())==0:
                logger.debug("Adding Playlist")
                db.add_playlist("Liked Songs")
            if len(db.filter_row("albums", "name", tracks[id]["album"]).get_output())==0:
                logger.debug("Adding Albums")
                db.add_album(tracks[id]["album"], tracks[id]["album_artist"], img_url=tracks[id]["album-image-url"])
            local_id = db.add_song(tracks[id]["name"], tracks[id]["artist"], tracks[id]["album"], "Liked Songs", track_order=tracks[id]["track_number"])
            db.add_id(local_id, "Spotify", id)

        db.commit()
        db.close()

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

