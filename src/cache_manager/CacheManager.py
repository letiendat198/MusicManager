import os

from src.utils.FileHelper import FileHelper
import src.models.ResolveImageUrl as ResolveImageUrl

class _CacheManager:
    # Handle adding file to cache and safely returning data from a cache path in case of sudden deletion
    # Also handle deleting as well
    def __init__(self):
        self.path = "cache/"
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def cache_image_from_url(self, url, file_name) -> str:
        img_data = ResolveImageUrl.get_data_from_url(url)

        path = os.path.join(self.path, file_name)
        f = open(path, 'wb+')
        f.write(img_data)
        f.close()
        return path

        

cache_manager = _CacheManager()
def get_manager_instance():
    return cache_manager