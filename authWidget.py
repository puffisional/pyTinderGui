from PyQt5.QtWidgets import QWidget

import pyTinderGui.fb_auth_token as tFb
import pyTinderGui.phone_auth_token as tPhone
import pyTinderGui.tinderApi as tApi
from pyTinderGui.gui.authTemplate import Ui_Form


class AuthWidget(QWidget, Ui_Form):
    codeSent = False
    logCode = None

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

    def login(self):
        fbLogin, fbPass = self.facebookLoginInput.text(), self.facebookPassInput.text()
        mobileNumber = self.mobilePhoneInput.text()
        mobileToken = self.mobileTokenInput.text()

        if self.logCode is not None and mobileNumber != "" and mobileToken != "":
            token = tPhone.getToken(mobileNumber, mobileToken, self.logCode)
        else:
            accessToken = tFb.get_fb_access_token(fbLogin, fbPass)
            userId = tFb.get_fb_id(accessToken)
            token = tFb.get_auth_token(accessToken, userId)

        with open("./credentials.conf", "w+") as crd:
            crd.write(token)

        tApi.token = token
        from pyTinderGui.mainWidget import MainWidget
        mainWidget = MainWidget()

        def close(*args):
            mainWidget.running.clear()

        self.window().closeEvent = close
        self.window().setCentralWidget(mainWidget)

    def sendMobileCode(self):
        mobileNumber = self.mobilePhoneInput.text()
        if mobileNumber != "":
            self.logCode = tPhone.sendCode(mobileNumber)
            return
