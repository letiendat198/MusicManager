import spotipy
import re
import os
import logging
from spotipy.oauth2 import SpotifyOAuth
from src.utils.DatabaseHelper import DatabaseHelper, TrackObj

import src.cache_manager.CacheManager as CacheManager


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
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

        tracks = []
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
                album = track["album"]["name"]
                album_img_url = track["album"]["images"][0]["url"]


                track_obj = TrackObj(
                    song_id= track["id"],
                    song_name= name,
                    song_artists= artists,
                    album_name = album,
                    album_artists=album_artist,
                    track_order=track_number,
                    album_img_url=album_img_url
                )
                tracks.append(track_obj)
            if count>100: break

        db = DatabaseHelper()
        db.add_songs_to_db(tracks, "Liked Songs")

        for track in tracks:
            sanitized_file_name = re.sub('[\\/?:*"<>|]', '', track.album_name)
            file_name = sanitized_file_name + ".jpg"
            cache_path = CacheManager.get_manager_instance().cache_image_from_url(track.album_img_url, file_name)
            db.update_row("albums", "album_name", track.album_name, "img_path", cache_path)

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
                        "album_img_url": track["album"]["images"][0]["url"],
                        "source": "Spotify",
                    }
                }
                obj.update(track_dict)
                print(obj)


