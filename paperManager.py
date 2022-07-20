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
from ui_functions import myApp

app = myApp()
app.run()