# Music Manager (WIP)
Is your music scattered all over the place? \
Are you tired of having to download them all individually? \
Are you broke and can't buy Spotify Premium but still want offline music? \
Am I the only person who have these issues?

No? Then this app is perhaps for you 

## Download
Download from [release](https://github.com/letiendat198/MediaManager/releases)

## Features
- Get liked tracks and playlists from Spotify
- Get individual Youtube video
- Search for the corresponding video on Youtube
- Download from Youtube
- Edit and write metadata (image included)

## TODO
- ~~Add Batch download Youtube~~
- ~~Allow user to specify download path~~
- ~~Change to id based storage~~
- ~~Create a DataHandler to handle all those playlist and stuffs~~
- ~~Fetch album data from Spotify and show it~~
- ~~Allow to add a Spotify playlist~~
- ~~Allow to add a Youtube video~~ and playlist (I don't use YT playlist much so this gonna be put off :D)
- ~~Refresh yt-title when yt-url is changed~~
- ~~Show tracks separated by playlist~~ (And sorted by A-Z)
- ~~Batch get url skip songs that already have url~~
- ~~Store mp3 path info of songs~~
- ~~Validate downloaded info~~ (When hit Refresh) (Investigate missing downloads too - Probably overlapping song names)
- ~~Auto change mp3 metadata with supplied info~~ (When download, click "Save" or do Batch write metadata. Batch download 
not gonna write metadata. Write batch metadata manually)
- ~~Limit QThreadpool to something more reasonable so that 
Chrome webdriver not gonna murder someone machine~~ (Make a setting menu to set this too. Also 6 threads seems resonable)
- ~~Show album image~~ ~~(Rework showing logic: Prioritize embeded image)~~
- ~~Allow user to add album image~~
- ~~Delete button should delete downloaded track~~

Seems ready for release! More features will be added later when I feel like it :D
- Allow user to add a mp3 file as download-path for songs
- Do import json
- Get track num?
- Add a settings menu
- Add icon to specify music source
- Change popups to actually look decent
- Make progress bar

## Issues tracker
- ~~Flickering popups~~ (Turns out you don't init QWidget many times. And don't restate UI elements many time. 
Just handle dynamic stuffs in a seperate function. Somehow only affected Download and Search)
- ~~Image chooser keep reopen~~ (Do not write .connect() in somewhere that run multiple time)
- ~~Song with same name will overlap when download~~ (File name now come with artist)
- ~~Delete button (Also other buttons too but less obvious) firing n times when used n times~~ (Again, do not write
.connect() somewhere it will be called multiple times)
- DataManager takes 2 update first time to generate working data.json
- Batch get url won't close automatically
- A few things will crash randomly cause I can't squash all bugs (TODO: Add a logging system)
- Sometimes batch operations will fail with no apparent cause (More threads more fails)
- Will add when remember
