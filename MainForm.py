# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainForm(object):
    def setupUi(self, mainForm):
        mainForm.setObjectName("mainForm")
        mainForm.resize(403, 308)
        self.centralwidget = QtWidgets.QWidget(mainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.labelCounter = QtWidgets.QLabel(self.centralwidget)
        self.labelCounter.setGeometry(QtCore.QRect(30, 180, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.labelCounter.setFont(font)
        self.labelCounter.setMidLineWidth(0)
        self.labelCounter.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCounter.setObjectName("labelCounter")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 220, 381, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonMinus = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.buttonMinus.setFont(font)
        self.buttonMinus.setObjectName("buttonMinus")
        self.horizontalLayout.addWidget(self.buttonMinus)
        self.buttonPlus = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.buttonPlus.setFont(font)
        self.buttonPlus.setObjectName("buttonPlus")
        self.horizontalLayout.addWidget(self.buttonPlus)
        self.messageTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.messageTextEdit.setGeometry(QtCore.QRect(30, 30, 341, 131))
        self.messageTextEdit.setObjectName("messageTextEdit")
        mainForm.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainForm)
        QtCore.QMetaObject.connectSlotsByName(mainForm)

    def retranslateUi(self, mainForm):
        _translate = QtCore.QCoreApplication.translate
        mainForm.setWindowTitle(_translate("mainForm", "MainWindow"))
        self.labelCounter.setText(_translate("mainForm", "0"))
        self.buttonMinus.setText(_translate("mainForm", "-"))
        self.buttonPlus.setText(_translate("mainForm", "+"))

