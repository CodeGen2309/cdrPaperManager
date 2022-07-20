import time
import requests
import os

from threading import Thread
from PySide2.QtCore import *
from bs4 import BeautifulSoup

class paperConnector (QObject):
    tdownSignal = Signal(str, dict)

    def __init__ (self):
        super().__init__()
        self.firstPageLink = 'https://wallpaperscraft.ru'
        self.categories = self.getCategories()


    def getCategories (self):
        res = requests.get(self.firstPageLink)
        firstPage = BeautifulSoup(res.text, 'lxml')
        cats = firstPage.find(class_='filters__list').find_all(class_='filter__link')
        catsarr = []

        for cat in cats:
            category = {}
            catLink = cat.attrs['href']
            catText = cat.text.replace('\n', '').lstrip()
            count = cat.find('span').text

            catText = catText.replace(count, '')
            catText = f'{catText} ({count})'
            category = {'text': catText, 'link': self.firstPageLink + catLink}

            catsarr.append(category) 

        return catsarr


    def getImagesLinks (self, page = None):
        if page == None: page = self.firstPageLink

        res = requests.get(page)
        content = BeautifulSoup(res.text, 'lxml')
        imgItems = content.find_all(class_='wallpapers__item')
        images = []

        for item in imgItems:
            thumbLink = item.find('img')
            fullLink = thumbLink.attrs['src'].split('_')

            lastEl = fullLink[-1].split('.')
            lastEl[0] = '1920x1080'
            lastEl = '.'.join(lastEl)

            fullLink[-1] = lastEl

            image = {
                'fileName': f'{fullLink[1]}_{fullLink[2]}',
                'fullLink': '_'.join(fullLink),
                'thumbLink': thumbLink.attrs['src']
            }

            images.append(image)

        return images


    def downloadImage (self, imageLink, imageName = 'defaulName', imgFolder = 'images'):
        image = requests.get(imageLink)
        imagePath = f'{imgFolder}/{imageName}.jpg'

        if not os.path.isdir(imgFolder): os.mkdir(imgFolder)
        with open(imagePath, 'wb') as f: f.write(image.content)
        return imagePath



class thumbDownloaderThread (QThread):
    thumbIsDownloaded = Signal(str, dict)

    def __init__ (self, pages):
        super().__init__()
        self.pages = pages

    def getImagesLinks (self, page):
        res = requests.get(page)
        content = BeautifulSoup(res.text, 'lxml')
        imgItems = content.find_all(class_='wallpapers__item')
        images = []

        for item in imgItems:
            thumbLink = item.find('img')
            fullLink = thumbLink.attrs['src'].split('_')

            lastEl = fullLink[-1].split('.')
            lastEl[0] = '1920x1080'
            lastEl = '.'.join(lastEl)

            fullLink[-1] = lastEl

            image = {
                'fileName': f'{fullLink[1]}_{fullLink[2]}',
                'fullLink': '_'.join(fullLink),
                'thumbLink': thumbLink.attrs['src']
            }

            images.append(image)

        return images


    def downloadImage (self, imageLink, imageName, imgFolder = 'thumbs'):
        image = requests.get(imageLink)
        imagePath = f'{imgFolder}/{imageName}.jpg'

        if not os.path.isdir(imgFolder): os.mkdir(imgFolder)
        with open(imagePath, 'wb') as f: f.write(image.content)
        return imagePath


    def run (self):
        for page in self.pages:
            links = self.getImagesLinks(page)

            for link in links:
                path =  self.downloadImage(link['thumbLink'], link['fileName'])
                self.thumbIsDownloaded.emit(path, link)







if __name__ == '__main__':
    test = thumbDownloaderThread([
        'https://wallpaperscraft.com/',
        'https://wallpaperscraft.com/catalog/dark',
        'https://wallpaperscraft.com/catalog/minimalism'
    ])
    test.run()
