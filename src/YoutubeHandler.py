import os
import re
import yt_dlp as youtube_dl
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_url(id, search_query, progress_callback=None):
    print("Searching url for " + search_query)
    query = urllib.parse.quote(search_query)
    search_url = "https://www.youtube.com/results?search_query=" + query
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_option)
    driver.get(search_url)
    titles = driver.find_elements(By.CSS_SELECTOR,
                                  "a.yt-simple-endpoint.style-scope.ytd-video-renderer")  # if shits break it gonna be this
    elem = titles[0]
    link = elem.get_attribute("href")
    title = elem.get_attribute("title")
    print(link)
    driver.quit()
    return id, link, title


def download(url, name, id, path, progress_callback=None):
    name = re.sub('[\\/?:*"<>|]', '', name)
    file_path = os.path.join(path, name)
    options = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': file_path + ".%(ext)s",
        'writethumbnail': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'},
            {'key': 'EmbedThumbnail'}],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(url)
    return id, file_path + ".mp3"


def get_info(id, url, progress_callback=None):
    options = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'quiet': 'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
        yt_id = info.get("id", None)
        title = info.get("title", None)

    return id, yt_id, title, url


def get_playlist_info(url, progress_callback=None):
    options = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    playlist_data = {}
    with youtube_dl.YoutubeDL(options) as ydl:
        playlist_info = ydl.extract_info(url, download=False)

        for info in playlist_info["entries"]:
            yt_id = info.get("id", None)
            title = info.get("title", None)
            playlist_data[yt_id] = {
                "name": title,
                "artist": "",
                "album": "",
                "source": "Youtube",
                "yt-url": "https://www.youtube.com/watch?v=" + yt_id,
                "yt-title": title
            }

    return playlist_info["title"], playlist_data