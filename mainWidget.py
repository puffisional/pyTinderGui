import datetime
import time
from threading import Thread, Event

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout

import pyTinderGui.tinderApi as tApi
from pyTinderGui import ACTION_DISLIKE, ACTION_STAR, ACTION_LIKE
from pyTinderGui.cardLastMatchWidget import CardLastMatchWidget
from pyTinderGui.cardWidget import CardWidget
from pyTinderGui.gui.mainTemplate import Ui_Form


class MainWidget(QWidget, Ui_Form):
    sigStatus = pyqtSignal(str, str, int, int, str)
    sigAddCard = pyqtSignal(object)
    sigBufferCard = pyqtSignal(object)
    gridPointer = (0, 0)
    version = 0.2
    maxVisibleCards = 10
    cardBufferSize = 15
    running = Event()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.cards = []
        self.running.set()
        self.peopleFilter = []
        self.refreshEvent = Event()
        self.refreshEvent.set()
        self.sigStatus.connect(self.setStatus)
        self.sigAddCard.connect(self.addCard)
        self.sigBufferCard.connect(self.bufferCard)
        self.setupUi(self)
        cbw = QWidget(self)
        self.cardBuffer = QHBoxLayout(cbw)
        cbw.hide()
        self.versionLabel.setText("Marian@Tinder {}".format(self.version))
        self.getLastMatch()
        Thread(target=self.refreshMyInfo).start()
        Thread(target=self._refreshThread).start()

    def addCard(self, card):
        x, y = self.gridPointer
        y += 1
        if y % 6 == 0:
            x += 1
            y = 1
        self.scrollAreaWidgetContents.layout().addWidget(card, x, y - 1)
        self.gridPointer = (x, y)
        self.cards.append(card)

    def bufferCard(self, cardContent):
        personId = cardContent[u"user"]['_id']
        if personId not in self.peopleFilter:
            self.peopleFilter.append(personId)
            card = CardWidget(cardContent)
            card.sigCardAction.connect(self.cardAction)
            self.cardBuffer.addWidget(card)

    @pyqtSlot()
    def logout(self):
        print("out")

    @pyqtSlot()
    def refresh(self):
        for card in self.cards[1:]:
            card.setParent(None)
            QApplication.processEvents()

        self.cards = self.cards[:1]
        self.gridPointer = (0, 1)

    @pyqtSlot(str, str, int, int, str)
    def setStatus(self, long, lat, likes, superLikes, waitUntil):
        self.locationInput.setText("{}, {}".format(long, lat))
        self.likesLeft.setValue(likes)
        self.superLikesLeft.setValue(superLikes)

        if waitUntil == '':
            self.likesLeftWaitInput.hide()
        else:
            self.likesLeftWaitInput.show()
            self.likesLeftWaitInput.setText(waitUntil)

    @pyqtSlot(int, object)
    def cardAction(self, action, card):
        cardIndex = self.cards.index(card)
        personId = card.personId
        row, column = self.getCardCoords(card)
        newCard = self.cardBuffer.itemAt(0).widget()

        # del self.cards[cardIndex]
        self.scrollAreaWidgetContents.layout().addWidget(newCard, row, column)
        self.cards[cardIndex] = newCard
        card.setParent(None)
        del card

        def _finish():
            if action == ACTION_DISLIKE:
                tApi.dislike(personId)
            elif action == ACTION_LIKE:
                tApi.like(personId)
            elif action == ACTION_STAR:
                tApi.superlike(personId)

        Thread(target=_finish).start()

    def getLastMatch(self):
        matchesCount, self.lastMatchImageData = tApi.fast_match_info()
        self.lmc = CardLastMatchWidget(self.lastMatchImageData, matchesCount)
        self.addCard(self.lmc)

    def getCardCoords(self, card):
        for i in range(self.scrollAreaWidgetContents.layout().rowCount()):
            for j in range(self.scrollAreaWidgetContents.layout().columnCount()):
                cardAt = self.scrollAreaWidgetContents.layout().itemAtPosition(i, j)
                if cardAt is not None and cardAt.widget() == card:
                    return i, j

    def getNextFinishedCard(self, r, c):
        fromIndex = r + 1 * c + 1
        index = 1
        for i in range(self.scrollAreaWidgetContents.layout().rowCount()):
            for j in range(self.scrollAreaWidgetContents.layout().columnCount()):
                if index < fromIndex: continue
                cardAt = self.scrollAreaWidgetContents.layout().itemAtPosition(i, j)
                if cardAt is not None and cardAt.widget().loaded:
                    return i, j, cardAt.widget()
                index += 1

    def refreshMyInfo(self):
        waitUntil = None
        meta = tApi.get_meta()
        me = tApi.get_self()
        lat, long = me["pos"]["lat"], me["pos"]["lon"]
        likes, superLikes = meta['rating']['likes_remaining'], meta['rating']['super_likes']['remaining']
        if likes == 0:
            remainingTime = str(meta['rating']['rate_limited_until'])[:-3]
            waitUntil = datetime.datetime.fromtimestamp(
                int(remainingTime)
            ).strftime('%Y-%m-%d %H:%M:%S')

        self.sigStatus.emit(str(lat), str(long), likes, superLikes, waitUntil)

    @pyqtSlot(str)
    def showPeople(self, count):
        self.maxVisibleCards = int(count)
        self.refresh()

    def _refreshThread(self):
        infoUpdateCounter = 6

        while self.running.isSet():
            if self.cardBuffer.count() < self.cardBufferSize:
                recommendations = tApi.get_recs_v2()
                for result in recommendations["data"]["results"]:
                    self.sigBufferCard.emit(result)
            self._rebuff()
            if infoUpdateCounter == 0:
                self.refreshMyInfo()
                infoUpdateCounter = 6
            infoUpdateCounter -= 1
            time.sleep(1)

    def _rebuff(self):
        if len(self.cards) < self.maxVisibleCards:
            diff = self.maxVisibleCards - len(self.cards)
            for cardIndex in range(self.cardBuffer.count()):
                bufferedCard = self.cardBuffer.itemAt(cardIndex)
                if bufferedCard is not None and bufferedCard.widget().loaded:
                    self.sigAddCard.emit(bufferedCard.widget())
                    diff -= 1
                if diff <= 0:
                    break