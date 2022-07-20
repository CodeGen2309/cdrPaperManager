import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class mainUI (QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)

        super().__init__()
        self.setupUI()
        self.setupStyles()


    def setupUI (self):
        self.resize(1050, 600)
        self.setWindowTitle('Paper Manager')

        self.centralWidget = QFrame()
        self.centralWidget.setObjectName('centralWidget')
        self.setCentralWidget(self.centralWidget)

        self.header = QFrame(self.centralWidget)
        self.header.setObjectName('header')
        self.header.resize(1050, 30)

        self.headerLay = QHBoxLayout()
        self.headerLay.setContentsMargins(0, 0, 0, 0)
        self.headerLay.setSpacing(0)
        self.header.setLayout(self.headerLay)

        self.header.catButton = QPushButton('Разделы')
        self.header.catButton.setObjectName('header__categories')
        self.headerLay.addWidget(self.header.catButton)

        self.headerLay.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.contentHolder = QScrollArea(self.centralWidget)
        self.contentHolder.setGeometry(0, 30, self.width(), self.height() - 30)
        self.contentHolder.setContentsMargins(0, 0, 0, 0)
        self.contentHolder.setObjectName('content__holder')
        self.contentHolder.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.contentHolder.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.contentFrame = QFrame(self.contentHolder)
        self.contentFrame.resize(self.width(), 1000)
        self.contentFrame.setObjectName('content')
        self.contentHolder.setWidget(self.contentFrame)

        self.catPages = QFrame(self.centralWidget)
        self.catPages.setObjectName('catPages')
        self.catPages.setGeometry(0, self.height() - 70, self.width(), 50)

        self.catPages.lay = QHBoxLayout()
        self.catPages.lay.setContentsMargins(0, 0, 0, 0)
        self.catPages.lay.setSpacing(0)
        self.catPages.setLayout(self.catPages.lay)

        self.sideBar = QFrame(self.centralWidget)
        self.sideBar.setObjectName('sideBar')
        self.sideBar.setGeometry(0, 30, 0, 400)
        self.sideBar.setContentsMargins(0, 0, 0, 0)

        self.sideBar.lay = QVBoxLayout()
        self.sideBar.lay.setMargin(0)
        self.sideBar.lay.setContentsMargins(0, 0, 0, 0)
        self.sideBar.setLayout(self.sideBar.lay)

        self.sideBar.itemsMenu = QStackedWidget()
        self.sideBar.itemsMenu.setObjectName('sideBar__menu')
        self.sideBar.lay.addWidget(self.sideBar.itemsMenu)

        self.sideBar.lay.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.sideBar.pages = QFrame()
        self.sideBar.pages.setObjectName('sideBar__pages')
        self.sideBar.lay.addWidget(self.sideBar.pages)

        self.sideBar.pages.lay = QHBoxLayout()
        self.sideBar.pages.lay.setContentsMargins(0, 0, 0, 0)
        self.sideBar.pages.lay.setSpacing(0)
        self.sideBar.pages.setLayout(self.sideBar.pages.lay)

        self.statusBar = QFrame(self.centralWidget)
        self.statusBar.setGeometry(0, self.height() - 20, self.width(), 20)
        self.statusBar.setObjectName('statusBar')

        self.statusLay = QHBoxLayout()
        self.statusLay.setContentsMargins(5, 0, 0, 0)
        self.statusLay.setSpacing(0)
        self.statusBar.setLayout(self.statusLay)

        self.statusBar.label = QLabel()
        self.statusBar.label.setObjectName('statusBar__label')
        self.statusLay.addWidget(self.statusBar.label)


    def setupStyles (self):
        self.mainStyles = '''
            #centralWidget {background: #45187f}

            #header {background: #391469}
            #header__categories:hover {background: rgba(255, 255, 255, .1)}
            #header__categories {
                background: transparent;
                min-height: 30px;
                min-width: 200px;
                font-size: 12px;
                color: white;
                border: none;
            }

            #header__winButton {min-width: 50px; min-height: 30px; border: none; background: transparent}
            #header__winButton:hover {background: rgba(255, 255, 255, .1)}

            #content {background: transparent}
            #content__holder {border: none; background: transparent}

            #sideBar {background: #391469}
            #sideBar__menu {}
            #sideBar__menuItem {background: transparent; color: white; border: none; min-height: 30px;}
            #sideBar__menuItem:hover {background: rgba(255, 255, 255, .1); color: white}
            #sideBar__pages {min-height: 30px}
            #sidebar__pagesItem {background: transparent; color: white; min-height: 30px; border: none;}
            #sidebar__pagesItem:hover {background: rgba(255, 255, 255, .1)}


            #CategoryItem {
                background: rgba(0, 0, 0, .1);
                color: white;
            }

            #HeaderIcon {
                background: transparent;
                color: white;
            }        

            #imageBox__button {background: #391469; border: none; min-height: 25px;}
            #imageBox__button:hover {background: rgba(255, 255, 255, .1)}

            #catPages {}
            #catPages__item:hover {background: rgba(255, 255, 255, .1);}
            #catPages__item {
                min-height: 20px;
                max-width: 40px; 
                color: white; 
                border: none;
                background: #391469;
            }

            #statusBar {background: #391469}
            #statusBar__label {min-height: 20px; min-width: 700px; color: #7f8c8d}
            #statusBar__resize {max-width: 30px; background: transparent; border: none}

        '''

        self.centralWidget.setStyleSheet(self.mainStyles)
  
  
    def run (self):
        self.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    app = mainUI()
    app.run()