import datetime
from threading import Thread

import requests
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from pyTinderGui import ACTION_DISLIKE, ACTION_LIKE, ACTION_STAR
from pyTinderGui.gui.cardTemplate import Ui_Form


class CardWidget(QWidget, Ui_Form):
    sigMainPhoto = pyqtSignal(object)
    sigThumbPhoto = pyqtSignal(str, object)
    sigCardAction = pyqtSignal(int, object)
    action = None
    personId = None
    loaded = False

    def __init__(self, cardContent, parent=None):
        QWidget.__init__(self, parent)
        self.cardContent = cardContent
        self.sigMainPhoto.connect(self.displayMainPhoto)
        self.sigThumbPhoto.connect(self.displayThumbPhoto)
        self.personId = cardContent[u"user"]['_id']
        self.setupUi(self)

    def setupUi(self, Form):
        Ui_Form.setupUi(self, self)
        now = datetime.datetime.now()
        userInfo = self.cardContent[u"user"]
        bio = userInfo[u"bio"]
        name = userInfo[u"name"]
        distance = round(self.cardContent[u"distance_mi"] * 1.60934)
        age = now.year - int(userInfo[u"birth_date"][:4])

        photos = userInfo[u"photos"]
        self.nameLabel.setText("{}, {}".format(name, age))
        self.distanceLabel.setText("{} km".format(distance))
        Thread(target=self._loadMainPhoto, args=(photos[0]['url'],)).start()

        thumbs = []
        for photo in photos:
            thumbs.append((photo['url'], photo['processedFiles'][-1]))

        Thread(target=self._loadThumbs, args=(thumbs,)).start()

        def mpe(event):
            if event.button() == Qt.RightButton:
                self.dislike(True)
            elif event.button() == Qt.LeftButton:
                self.like(True)

        self.photosFrame.mousePressEvent = mpe

    def _loadMainPhoto(self, url):
        data = requests.get(url).content
        self.sigMainPhoto.emit(data)

    def _loadThumbs(self, thumbUrls):
        for index, (bigUrl, thumb) in enumerate(thumbUrls[:7]):
            data = requests.get(thumb["url"]).content
            self.sigThumbPhoto.emit(bigUrl, data)
        self.loaded = True

    def like(self, flag):
        if flag:
            self.action = ACTION_LIKE
            self.sigCardAction.emit(self.action, self)

    def dislike(self, flag):
        if flag:
            self.action = ACTION_DISLIKE
            self.sigCardAction.emit(self.action, self)

    def star(self, flag):
        if flag:
            self.action = ACTION_STAR
            self.sigCardAction.emit(self.action, self)

    @pyqtSlot(object)
    def displayMainPhoto(self, imgData):
        image = QImage()
        image.loadFromData(imgData)
        si = image.scaledToWidth(682)

        lbl = QLabel(self)
        lbl.setPixmap(QPixmap(si))
        self.photosFrame.layout().addWidget(lbl, 0, 0)

    @pyqtSlot(str, object)
    def displayThumbPhoto(self, bigUrl, imgData):
        image = QImage()
        image.loadFromData(imgData)
        si = image.scaledToWidth(87)

        lbl = QLabel(self)
        lbl.setPixmap(QPixmap(si))
        self.thumbList.layout().addWidget(lbl)

        def mousePressEvent(*args):
            Thread(target=self._loadMainPhoto, args=(bigUrl,)).start()
            return QWidget.mousePressEvent(lbl, *args)

        lbl.mousePressEvent = mousePressEvent
