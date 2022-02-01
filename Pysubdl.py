#!/usr/bin/env python3
# coding:utf-8

import requests
from bs4 import BeautifulSoup
import os
import shutil
from zipfile import ZipFile
import platform

osName = platform.system()

webSiteUrl = "https://subf2m.co"

language = {
    "Persian": "farsi_persian",
    "English": "english",
    "Arabic": "arabic",
}

formatMovie = {
    "WEB-DL": "WEB-DL",
    "WEBRip": "WEBRip",
    "HDTV": "HDTV",
    "HDRip": "HDRip",
    "HC-Cam": "HC-Cam",
    "HDTC": "HDTC",
    "HC.CAMRip": "HC.CAMRip",
    "HC.HDTS": "HC.HDTS",
    "HD-TC": "HD-TC",
    "BluRay": "BluRay",
    "UHD.BluRay": "UHD.BluRay",
    "BRRip": "BRRip",
    "BDRip": "BDRip",
    "Full.HD": "Full.HD",
    "HDCam": "HDCam",
}

resolution = {
    "720": "720",
    "480": "480",
    "1080": "1080",
    "2160": "2160",
}

getlanguage = "Persian"
getNameMovie = "deadpool"
getFormat = "720"
getResolotion = "BluRay"

currentPath = os.getcwd()
path = os.path.join(currentPath, getNameMovie.capitalize())
try:
    if os.path.exists(getNameMovie.capitalize()):
        print(getNameMovie.capitalize() + " in directory has exist.Please remove " +
              getNameMovie.capitalize() + " in directory and try again")
        exit(0)

    os.makedirs(path, exist_ok=True)

except OSError as error:
    print("Directory '%s' can not be created" % getNameMovie.capitalize())

getNameMovie = getNameMovie.replace(" ", "+")
getNameMovie = getNameMovie.lower()

searchUrl = webSiteUrl + "/subtitles/searchbytitle?query=" + getNameMovie + "&l="

getPage = requests.get(searchUrl)
getInfoPage = BeautifulSoup(getPage.content, "html5lib")

searchName = getInfoPage.find("div", {"class": "title"})
nameMovieFound = searchName.get_text()

nameMovieFound = nameMovieFound.lower()
nameCheckMovie = getNameMovie.split()

for check in nameCheckMovie:
    if check not in nameMovieFound:
        exit(0)


searchMovieUrl = webSiteUrl + searchName.find("a").get("href") + "/" + language[getlanguage]

getPage = requests.get(searchMovieUrl)
getInfoPage = BeautifulSoup(getPage.content, "html5lib")

posterUrl = getInfoPage.find("div", {"class": "poster"}).find("img").get("src")

subtitleUrl = []
for item in getInfoPage.find_all("li", {"class": "item"}):
    for list in item.find_all("ul", {"class": "scrolllist"}):
        if getFormat in list.text and getResolotion in list.text:
            subtitleUrl.append(
                webSiteUrl + item.find("a", {"class": "download icon-download"}).get("href"))

linkDownload = []
for page in subtitleUrl:
    getPage = requests.get(page)
    getInfoPage = BeautifulSoup(getPage.content, "html5lib")
    linkDownload.append(webSiteUrl + getInfoPage.find("a", {"class": "button positive"}).get("href"))


if osName == "Windows":

    count = 1
    for link in linkDownload:
        filename = getNameMovie + str(count) + ".zip"
        count += 1
        req = requests.get(link)
        with open(filename, "wb") as f:
            for chunk in req.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    filesToMove = []
    for i in range(len(linkDownload)):
        filesToMove.append(getNameMovie + str(i + 1) + ".zip")


    for file in filesToMove:
        source = currentPath + "\\" + file
        destination = path + "\\" + file
        shutil.move(source, destination)


    for file in filesToMove:
        with ZipFile(path + "\\" + file, 'r') as zip:
            zip.extractall(path)


    for file in filesToMove:
        os.remove(path + "\\" + file)
