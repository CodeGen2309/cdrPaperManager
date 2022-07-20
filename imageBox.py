import sys
import requests

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class imageBox (QWidget):
    def __init__ (self, parent = None, imgFile = None, width = 200):
        super(imageBox, self).__init__(parent)

        # Создаем нужные обьекты
        self.mainLay = QVBoxLayout()
        self.imgHolder = QLabel()
        self.iconsHolder = QFrame()
        self.iconsLay = QHBoxLayout()
        self.img = QPixmap(imgFile)
        self.imgRels = self.img.height() / self.img.width()


        # Даем им имена
        self.setObjectName('imageBox')
        self.imgHolder.setObjectName('imageBox__imgHolder')
        self.iconsHolder.setObjectName('imageBox__iconsHolder')
 
        # Основной код
        self.setLayout(self.mainLay)

        self.iconsLay.setContentsMargins(0, 0, 0, 0)
        self.iconsLay.setSpacing(0)

        self.img = self.img.scaled(width, width * 1, Qt.KeepAspectRatio)
        self.imgHolder.setPixmap(self.img)
        self.mainLay.addWidget(self.imgHolder)

        self.iconsHolder.setFixedHeight(30)
        self.iconsHolder.setLayout(self.iconsLay)
        self.mainLay.addWidget(self.iconsHolder)

        self.addFooterButtons()


    def addFooterButtons (self):
        self.wallButton = QPushButton()
        self.downloadButton = QPushButton()

        self.wallButton.setObjectName('imageBox__button')
        self.downloadButton.setObjectName('imageBox__button')

        self.wallButton.setIcon(QIcon('./icons/screen.svg'))
        self.downloadButton.setIcon(QIcon('./icons/download.svg'))

        self.iconsLay.addWidget(self.wallButton)
        self.iconsLay.addWidget(self.downloadButton)



if __name__ == '__main__':
    app = QApplication()

    imb = imageBox(imgFile='./thumbs/vektor_panorama.jpg', width=400)
    imb.show()

    sys.exit(app.exec_())