# Subtitles

 - Scripts for dealing with subtitles

## Renaming

 - [rename.py](rename.py)
 - Renames all srt files in the folder
  - defaults to matching `\d{2}x\d{2}` regex
  - can also match `[sS]\d{2}[eE]\d{2}` or based on similaritiy using difflib's [SequenceMatcher](https://docs.python.org/3/library/difflib.html)
  - will run into issues with multiple seasons in the same folder

## Downloading

 - [subscene.py](subscene.py)
 - command line tool to download from subscene
 - Workaround after using [Alfred](https://www.alfredapp.com/) to search for `https://subscene.com/subtitles/search='{query}'` was broken with an update
 - Uses [Selenium](https://pypi.org/project/selenium/) and [bs4](https://pypi.org/project/bs4/)

## Syncing

 - [subshift.py](subshift.py)
 - still a WIP
 - based on [SubShifter](https://subshifter.bitsnbites.eu/)

## Cleaning

 - [nohi.py](nohi.py)
 - removes hearing impaired lines and anything that isn't dialogue

## Extracting

 - [video2text](video2text)
 - Converts PGS to srt
 - Extracts a PGS subtitle stream from a mkv, splits it into images, ocrs the images, and writes to srt
 - Uses ffmpeg, mkvtoolnix, BDSup2Sub, bs4, pytesseract, imagemagick

