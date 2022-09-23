# u2dl

Terminal youtube video ▶️ downloader 📥

![u2dl-version](/docs/u2dl-v.gif)

[u2dl](https://github.com/Darkhound-org/u2dl) is a cli app made in python 🐍 that downloads videos from youtube. It processes and displays the streams and the user can select one from it or just type `h` to get the video in highest resolution. Downloaded videos can be further converted to mp3 format. You can specify the download path if you want with the `--save_to` or `-s` option.

## Installation
Users in Windows can download the latest binary from [releases](https://github.com/Darkhound-org/u2dl/releases) [standalone or single executable]. Alternatively, you can clone this repo, make a new `venv`, activate it , run `pip install -r requirements.txt` and then run the app `u2dl.py`.

### FFmpeg 
u2dl needs FFmpeg library (or just ffmpeg.exe) to convert video to mp3 format. It is recommended to keep the FFmpeg binaries along with the u2dl executable(or script) or add to system path. 

You can download FFmpeg from the official site or for just the ffmpeg.exe run `u2dl -f`.

### Try online
Try u2dl on Binder
 [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Darkhound-org/u2dl/HEAD)

 Open a bash terminal in binder and run `cd src`.
 Install the dependencies `pip install -r requirements.txt`.

 Now run the app `python u2dl.py` 

## Usage
Navigate to the directory where the binary(or script) is located and run `u2dl.exe`. 

**If you encouter a false positive virus warning make the app an exception in windows virus and threat protection (or in the virus scanner you are using).**





