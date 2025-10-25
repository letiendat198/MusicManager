import os
import logging

from src.utils.FileHelper import FileHelper
import src.models.ResolveImageUrl as ResolveImageUrl

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CacheManager:
    # Handle adding file to cache and safely returning data from a cache path in case of sudden deletion
    # Also handle deleting as well
    def __init__(self):
        self.path = "cache/"
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def cache_image_from_url(self, url, file_name, progress_callback=None) -> str:
        logger.debug("Caching file %s", file_name)
        img_data = ResolveImageUrl.get_data_from_url(url)

        path = os.path.join(self.path, file_name)
        f = open(path, 'wb+')
        f.write(img_data)
        f.close()

        logger.debug("File %s finished caching", file_name)
        return path
