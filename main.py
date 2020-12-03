#/usr/bin/python
import os, sys
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
binary = FirefoxBinary('C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
browser = webdriver.Firefox(firefox_binary=binary)

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def resizeImg(imgArr):
    print("resize begin")
    for index, imageList in enumerate(imgArr):
        try:
            print("proccesess picture: " + str(index) + "| of:" + str(len(imgArr)))
            img = Image.open(imageList["ImagePath"])
            oldSize = img.size
            new_width  = int(imageList["ImageWidth"])
            new_height = int(imageList["ImageHeight"])
            oldWidth = int(oldSize[0])
            oldHeight = int(oldSize[1])
            print("image path:")
            print(imageList["ImagePath"])
            if ( oldWidth>new_width and oldHeight>new_height ):
                print("image resizing...")
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
                img.save(imageList["ImagePath"],optimize=True,quality=85)
                print("image resized from:")
                print(str(oldWidth)+" x "+str(oldHeight))
                print("to:")
                print(str(new_width)+" x "+str(new_height))
        except Exception:
            print("File not found")
            pass

def GetImageArr (link):
    for index, article in enumerate(link):
        print("proccesess article: " + str(index) + "| of:" + str(len(link)))
        print("article url: " + str(article))
        browser.get(article)
        browser.maximize_window()
        time.sleep(2)
        elem = browser.find_elements_by_xpath('//img')
        resultArr = []
        for ii in elem:
            Image = ii
            artLink = Image.get_attribute('src')
            artLink = artLink.split('?', 1)[0]
            ImageWidth = str(Image.get_property("width"))
            ImageHeight = str(Image.get_property("height"))
            ImageLink = artLink
            ImageName = find_between_r(Image.get_attribute('src'),"/","?")
            ImagePath = "D:" + artLink.replace("http://sampleside-cdn.com", "")
            dict = {"ImageWidth":ImageWidth,"ImageHeight":ImageHeight,"ImageLink":ImageLink,"ImageName":ImageName,"ImagePath":ImagePath}
            resultArr.append(dict)
            del dict;
        resizeImg(resultArr)


def linkCycle( linkFile ):
    with open(linkFile) as f:
        linkList = f.readlines()
    imageArr = GetImageArr(linkList)
    print(linkList[12])
linkCycle("linklist.txt")