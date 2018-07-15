import argparse
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from pyTinderGui import TAPI_MOBILE
from pyTinderGui import tinderApi as tApi
from pyTinderGui.authWidget import AuthWidget
from pyTinderGui.mainWidget import MainWidget

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", default=TAPI_MOBILE)
    parser.add_argument("--number", default=u"")
    parser.add_argument("--fbUsername", default=u"")
    parser.add_argument("--fbPassword", default=u"")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("pyTinderGui")

    lm = tApi.lastMatch()
    if lm == b'Unauthorized':
        auth = AuthWidget()
        auth.facebookLoginInput.setText(args.fbUsername)
        auth.facebookPassInput.setText(args.fbPassword)
        auth.mobilePhoneInput.setText(args.number)
        win.setCentralWidget(auth)
    else:
        mw = MainWidget()
        def close(*args):
            mw.running.clear()

        win.closeEvent = close
        win.setCentralWidget(mw)


    win.show()
    app.exec()
