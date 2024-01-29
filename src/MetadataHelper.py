import eyed3
import urllib3

from FileHelper import *

class MetadataHelper:
    def __init__(self, path):
        self.track = eyed3.load(path)

    def write(self, obj, progress_callback=None):
        print("Writing metadata:", obj["name"], obj["artist"], obj["album"])
        self.track.tag.artist = obj["artist"]
        self.track.tag.album = obj["album"]
        self.track.tag.title = obj["name"]
        self.track.tag.album_artist = obj["artist"]

        self.track.tag.save()

    def add_image_from_url(self, url, progress_callback=None):
        print("Adding image to file via url", url)
        http = urllib3.PoolManager()
        resp = http.request("GET", url)
        for image in self.track.tag.images:
            self.track.tag.images.remove(image.description)
        self.track.tag.images.set(type_=3, img_data=resp.data, mime_type="image/jpeg")
        self.track.tag.save()

    def add_image_from_file(self, path, progress_callback=None):
        print("Adding image from file in", path)
        f = FileHelper(path)
        img_data = f.read_bytes()
        for image in self.track.tag.images:
            self.track.tag.images.remove(image.description)
        self.track.tag.images.set(type_=3, img_data=img_data, mime_type="image/jpeg")
        self.track.tag.save()

    def write_and_add_image(self, obj, url, progress_callback=None):
        self.write(obj)
        self.add_image_from_url(url)

    def get_album_image(self, progress_callback=None):
        for image in self.track.tag.images:
            return image.image_data
