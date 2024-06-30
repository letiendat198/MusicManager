import re
import sqlite3
import os
import logging
from typing import List
from typing_extensions import Self

logger = logging.getLogger(__name__)


class TrackObj:
    def __init__(self,
                 song_id=None,
                 song_name=None,
                 song_artists=None,
                 album_name=None,
                 album_artists=None,
                 track_order=None,
                 album_img_url=None,
                 album_img_path=None,
                 platform=None):
        self.platform = platform
        self.album_img_path = album_img_path
        self.album_img_url = album_img_url
        self.track_order = track_order
        self.album_artists = album_artists
        self.album_name = album_name
        self.song_artists = song_artists
        self.song_name = song_name
        self.song_id = song_id


class DatabaseHelper:
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(os.getcwd(), "database.db"))
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def init_database(self):
        self.cur.execute("PRAGMA foreign_keys = ON;")
        # self.cur.execute("DROP TABLE IF EXISTS ids")
        # self.cur.execute("DROP TABLE IF EXISTS songs")
        # self.cur.execute("DROP TABLE IF EXISTS playlists")
        # self.cur.execute("DROP TABLE IF EXISTS albums")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS songs(
            platform_id TEXT PRIMARY KEY, 
            song_name, 
            song_artist, 
            album, 
            track_order,  
            platform,
            ismn,
            FOREIGN KEY (album) REFERENCES albums(album_name)
            )""")
        self.cur.execute("CREATE TABLE IF NOT EXISTS albums(album_name PRIMARY KEY, album_artist, year, genre, img_url, img_path)")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS playlists(
            playlist_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            playlist_name
            )""")

    def add_song(self, id: str, name: str, artist: str, album: str, platform: str, track_order: int=None, ismn: str=None):
        # ID to NULL to use SQLite ROWID
        data = (id, name, artist, album, track_order, platform, ismn)
        self.cur.execute("INSERT INTO songs VALUES (?,?,?,?,?,?,?) RETURNING platform_id", data)
        return self.cur.fetchone()[0]

    def add_playlist(self, name: str) -> int:
        self.cur.execute("INSERT INTO playlists VALUES (?,?) RETURNING playlist_id", (None, name))
        id = self.cur.fetchone()[0]
        table_name = "playlist" + str(id)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS {}(
            track_id,
            FOREIGN KEY (track_id) REFERENCES songs(platform_id)
            )""".format(table_name))
        return id

    def add_album(self, name: str, artist: str, year: int=None, genre: str=None, img_url: str=None, img_path: str=None):
        data = (name, artist, year, genre, img_url, img_path)
        self.cur.execute("INSERT INTO albums VALUES (?,?,?,?,?,?)", data)

    def add_song_to_playlist(self, playlist_id: int, song_id: str):
        playlist_table = "playlist" + str(playlist_id)
        self.cur.execute("INSERT INTO {} VALUES (?)".format(playlist_table), (song_id,))

    def update_row(self, table: str, filter_column: str, condition: str, modify_column: str, new_value: str=None):
        self.cur.execute("UPDATE {} SET {} = ? WHERE {} = ?".format(table, modify_column, filter_column), (new_value, condition))

    def delete_row(self, table: str, column: str, condition: str):
        self.cur.execute("DELETE FROM {} WHERE {} = ?".format(table, column), (condition,))

    def filter_row(self, table: str, column: str, condition: str) -> Self:
        self.cur.execute("SELECT * FROM {} WHERE {}=?".format(table, column), (condition,))
        return self

    def get_all_from_table(self, table: str) -> List[sqlite3.Row]:
        self.cur.execute("SELECT * FROM {}".format(table))
        return self.cur.fetchall()

    def get_all_from_playlist(self, playlist_name: str) -> List[sqlite3.Row]:
        self.cur.execute("""SELECT * FROM {} 
                            INNER JOIN albums ON songs.album=albums.album_name 
                            INNER JOIN songs ON {}.track_id=songs.platform_id
                        """.format(playlist_name, playlist_name))
        return self.cur.fetchall()

    def count_row(self, table: str, column: str, condition: str) -> int:
        self.cur.execute("SELECT COUNT(*) FROM {} WHERE {}=?".format(table, column), (condition,))
        return self.cur.fetchone()[0]

    def get_output(self) -> List[sqlite3.Row]:
        return self.cur.fetchall()

    def commit(self):
        self.con.commit()
    def close(self):
        self.con.close()

    # High level utility function
    def add_songs_to_db(self, tracks: List[TrackObj], playlist_name: str):
        db = DatabaseHelper()
        db.init_database()

        playlist_id = None

        if db.count_row("playlists","playlist_name", playlist_name) == 0:
            logger.debug("Adding Playlist")
            playlist_id = db.add_playlist(playlist_name)
        else:
            playlist_id = db.filter_row("playlists", "playlist_name", playlist_name).get_output()[0]["playlist_id"]

        for track in tracks:
            logger.debug("Adding %s by %s from %s to db", track.song_name, track.song_artists, track.album_name)

            if db.count_row("albums", "album_name", track.album_name) == 0:
                logger.debug("Adding Albums %s", track.album_name)

                db.add_album(track.album_name, track.album_artists, img_url=track.album_img_url)

            db.add_song(track.song_id, track.song_name, track.song_artists, track.album_name, track.platform,
                                   track_order=track.track_order)
            db.add_song_to_playlist(playlist_id, track.song_id)

        db.commit()
        db.close()


