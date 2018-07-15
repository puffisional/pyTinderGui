from threading import Thread

import requests
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from pyTinderGui import tinderApi as tApi
from pyTinderGui.gui.cardLastMatchTemplate import Ui_Form


class CardLastMatchWidget(QWidget, Ui_Form):
    sigMainPhoto = pyqtSignal(object)
    sigMatchFound = pyqtSignal(str)
    sigSearchCounter = pyqtSignal(object)
    personId = None
    loaded = False
    searched = 0

    def __init__(self, cardContent, matchesCount, parent=None):
        QWidget.__init__(self, parent)
        self.sigMatchFound.connect(self.matchFound)
        self.sigSearchCounter.connect(self.updateSearch)
        self.cardContent = cardContent
        self.matchesCount = matchesCount
        self.setupUi(self)

    def setupUi(self, Form):
        Ui_Form.setupUi(self, self)
        self.allMatchCount.setText(self.matchesCount)
        self.displayMainPhoto(self.cardContent)

        for w in (self.pushButton_3, self.label, self.searchCounter, self.label_3):
            w.hide()

    @pyqtSlot(object)
    def updateSearch(self, imgData):
        self.searched += 1
        self.searchCounter.setText(str(self.searched))

        image = QImage()
        image.loadFromData(imgData)
        si = image.scaledToWidth(350)
        self.searchB.setPixmap(QPixmap(si))

    @pyqtSlot(str)
    def matchFound(self, matchToken):
        print(matchToken)

    @pyqtSlot(object)
    def displayMainPhoto(self, imgData):
        image = QImage()
        image.loadFromData(imgData)
        si = image.scaledToWidth(320)

        self.searchA = QLabel(self)
        self.searchA.setPixmap(QPixmap(si))
        self.photosFrame.layout().addWidget(self.searchA, 0, 0)

    @pyqtSlot()
    def reinit(self):
        self.matchesCount, self.cardContent = tApi.fast_match_info()
        self.setupUi(self)

    @pyqtSlot()
    def startSearch(self):

        def _search():
            peopleFilter = []
            while True:
                recommendations = tApi.get_recs_v2()
                print(recommendations)
                for result in recommendations["data"]["results"]:
                    personId = result[u"user"]['_id']
                    if personId in peopleFilter: continue
                    peopleFilter.append(personId)
                    photoUrl = result[u"user"][u"photos"][0]['processedFiles'][-1]['url']
                    data = requests.get(photoUrl).content
                    self.sigSearchCounter.emit(data)
                    if data == self.cardContent:
                        self.sigMatchFound.emit(personId)
                        break

        Thread(target=_search).start()
