import os
import yt_dlp as youtube_dl
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_url(name, search_query, progress_callback):
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
    return name, link, title


def download(url, name, path, progress_callback):
    options = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'outtmpl': os.path.join(path, name.replace("/", " "))+".%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(url)
    return name


def get_info(name, url, progress_callback):
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
        id = info.get("id", None)
        title = info.get("title", None)

    return name, id, title
