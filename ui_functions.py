import sys
import requests
import ctypes
import os

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from threading import Thread
from imageBox import imageBox
from connector import paperConnector, thumbDownloaderThread
from ui import mainUI


class myApp(mainUI):
    def __init__ (self):
        super().__init__()

        self.connector = paperConnector()
        self.downloaderThreads = []
        self.imgBoxes = []
        self.catButtons = []
        self.columnCount = 0

        self.header.catButton.clicked.connect(self.toggleSideBar)

        self.addCats(self.connector.categories) 
        self.downloaderThreads.append(self.getPagesThumbs([self.connector.firstPageLink]))

    def getPagesThumbs (self, pages):
        thr = thumbDownloaderThread(pages)
        thr.thumbIsDownloaded.connect(self.createImageBox)
        thr.start() 
        thr.quit()

        return thr

       
    def toggleSideBar (self):
        if self.sideBar.width() > 0:
            self.geometryAnim(self.sideBar, QRect(0, 30, 0, self.sideBar.height()), 400, easing=QEasingCurve.InOutCubic)
            self.fadeAnim(self.sideBar.itemsMenu, endVal=0)
            self.fadeAnim(self.sideBar.pages, endVal=0)

        else:
            self.geometryAnim(self.sideBar, QRect(0, 30, 200, self.sideBar.height()), duration=500)
            self.fadeAnim(self.sideBar.itemsMenu, 500)
            self.fadeAnim(self.sideBar.pages, 500)



    def fadeAnim (self, item, duration = 200, easing = QEasingCurve.InQuad, endVal = 1):
        if not hasattr(item, 'opacity'):
            item.opacity = QGraphicsOpacityEffect()
            item.fadeAnim = QPropertyAnimation(item.opacity, b'opacity')
            item.setGraphicsEffect(item.opacity)

        item.fadeAnim.setDuration(duration)
        item.fadeAnim.setEndValue(endVal)
        item.fadeAnim.setEasingCurve(easing)
        item.fadeAnim.start()
        

    def geometryAnim (self, item, newGeometry, duration = 200, easing = QEasingCurve.InOutCubic):
        item.animation = QPropertyAnimation(item, b'geometry')
        item.animation.setDuration(duration)
        item.animation.setEndValue(newGeometry)
        item.animation.setEasingCurve(easing)
        item.animation.start()


    def addCats (self, categories) :
        catOnPage = 1
        maxCatOnPage = 15

        button = None
        page = None

        for cat in categories:
            if catOnPage == maxCatOnPage: catOnPage = 1
            if catOnPage == 1: page = self.addMenuItemsPage()

            button = QPushButton(cat['text'])
            button.link = cat['link']
            button.setObjectName('sideBar__menuItem')
            button.clicked.connect(self.createImageBoxes)

            page.lay.addWidget(button)
            catOnPage = catOnPage + 1

        self.addSideBarPagesButtons(self.sideBar.itemsMenu.count())


    def addSideBarPagesButtons (self, pagesCount):
        for i in range(pagesCount):
            button = QPushButton(f'{i + 1}')

            button.setObjectName('sidebar__pagesItem')
            button.clicked.connect(self.changeMenuPage)

            self.sideBar.pages.lay.addWidget(button)


    def addMenuItemsPage (self):
        page = QFrame()
        page.lay = QVBoxLayout()

        page.lay.setContentsMargins(0, 0, 0, 0)
        page.setLayout(page.lay)

        self.sideBar.itemsMenu.addWidget(page)
        return page


    def changeMenuPage (self):
        newIndex = int(self.sender().text()) - 1
        self.sideBar.itemsMenu.setCurrentIndex(newIndex)

    
    def createImageBoxes (self):
        link = self.sender().link
        pagesLinks = []
        firstPage, lastPage, pagesInThread = 1, 16, 5

        for bx in self.imgBoxes: bx.deleteLater()
        self.imgBoxes = []

        for i in range(firstPage, lastPage, pagesInThread):
            for q in range(pagesInThread): pagesLinks.append(f'{self.sender().link}/page{q + i}')
            self.downloaderThreads.append(self.getPagesThumbs(pagesLinks))
            pagesLinks = []
            
        self.toggleSideBar()
        self.setStatusText(self.sender().link)


    def createImageBox (self, path, link):
        box = imageBox(self.contentFrame, path, width=250)

        box.iconsHolder.link = link['fullLink']
        box.iconsHolder.fileName = link['fileName']
        box.downloadButton.clicked.connect(self.downloadImage)
        box.wallButton.clicked.connect(self.setWallpaper)

        self.fadeAnim(box, duration=0, endVal=0)
        self.fadeAnim(box, 900, endVal=1)
        box.show()

        self.imgBoxes.append(box)
        self.setMasonry(cWidth=250)


    def setMasonry (self, cWidth = 200):
        columnCount = self.contentFrame.width() // cWidth
        boxInRow, boxCount = 0, 0
        boxHeight = self.imgBoxes[0].height() + 5
        gap = (self.width() - columnCount * cWidth) // (columnCount + 1)
        x, y = gap, gap

        if self.columnCount != columnCount:
            for i, box in enumerate(self.imgBoxes):
                box.move(x, y)

                x = x + cWidth + gap
                boxInRow = boxInRow + 1
                boxCount = boxCount + 1
                
                if boxInRow == columnCount:
                    x = gap
                    y = y + box.height() + gap
                    boxInRow = 0
                    
        #Удлиняем фрейм с боксами
        if i > 15: self.contentFrame.resize(self.width(), int(boxCount / columnCount + 0.5) * boxHeight)


    def downloadImage (self):
        self.setStatusText('Началась загрузка картинки')

        link = self.sender().parent().link
        fileName = self.sender().parent().fileName
        imgPath = self.connector.downloadImage(link, fileName)

        self.setStatusText(f'{fileName} загружена в папку images')
        return imgPath


    def setWallpaper (self):
        fileName = self.sender().parent().fileName
        imgPath = f'images/{fileName}.jpg'
        imgDownloaded = os.path.exists(imgPath)
        absPath = None
        SPI_SETDESKWALLPAPER = 20

        if not imgDownloaded: imgPath = self.downloadImage()
        absPath = os.path.abspath(imgPath)

        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absPath, 3)
        self.setStatusText(f'{imgPath} поставлена на работчий стол')


    def setStatusText (self, text):  self.statusBar.label.setText(text)
    def resizeEvent (self, *args):
        self.header.resize(self.width(), 30)
        self.sideBar.resize(self.sideBar.width(), self.height() - 50)
        self.contentHolder.resize(self.width(), self.height() - 50)
        self.contentFrame.resize(self.width(), self.height())
        self.statusBar.setGeometry(0, self.height() - 20, self.width(), 20)
        self.catPages.setGeometry(0, self.height() - 70, self.width(), 50)
        self.setMasonry(cWidth=250)



if __name__ == '__main__':
    app = myApp()
    app.run()