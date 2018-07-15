# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\authTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(846, 460)
        Form.setStyleSheet("QGroupBox {\n"
"border: 1px solid gray;\n"
"margin-top: 0.5em;\n"
"font-weight:bold;}\n"
"\n"
"QGroupBox::title {\n"
"subcontrol-origin: margin;\n"
"left: 10px;\n"
"padding: 0 3px 0 3px;\n"
"font-weight:bold}")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.mobilePhoneInput = QtWidgets.QLineEdit(self.groupBox_2)
        self.mobilePhoneInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.mobilePhoneInput.setObjectName("mobilePhoneInput")
        self.gridLayout_3.addWidget(self.mobilePhoneInput, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.mobileTokenInput = QtWidgets.QLineEdit(self.groupBox_2)
        self.mobileTokenInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.mobileTokenInput.setObjectName("mobileTokenInput")
        self.gridLayout_3.addWidget(self.mobileTokenInput, 1, 1, 1, 2)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.facebookLoginInput = QtWidgets.QLineEdit(self.groupBox)
        self.facebookLoginInput.setObjectName("facebookLoginInput")
        self.gridLayout_2.addWidget(self.facebookLoginInput, 0, 1, 1, 1)
        self.facebookPassInput = QtWidgets.QLineEdit(self.groupBox)
        self.facebookPassInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.facebookPassInput.setObjectName("facebookPassInput")
        self.gridLayout_2.addWidget(self.facebookPassInput, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.login)
        self.pushButton_2.clicked.connect(Form.sendMobileCode)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Zahlaš me"))
        self.groupBox_2.setTitle(_translate("Form", "Mobil autentifikácia"))
        self.label_3.setText(_translate("Form", "Číselko:"))
        self.label_4.setText(_translate("Form", "Token:"))
        self.pushButton_2.setText(_translate("Form", "Send"))
        self.groupBox.setTitle(_translate("Form", "Facebook autentifikácia"))
        self.label_2.setText(_translate("Form", "Heslo:"))
        self.label.setText(_translate("Form", "Login:"))

