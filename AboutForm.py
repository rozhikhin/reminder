# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AboutForm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutForm(object):
    def setupUi(self, AboutForm):
        AboutForm.setObjectName("AboutForm")
        AboutForm.resize(264, 169)
        self.labelProgramName = QtWidgets.QLabel(AboutForm)
        self.labelProgramName.setGeometry(QtCore.QRect(20, 30, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelProgramName.setFont(font)
        self.labelProgramName.setText("")
        self.labelProgramName.setObjectName("labelProgramName")
        self.labelAuthor = QtWidgets.QLabel(AboutForm)
        self.labelAuthor.setGeometry(QtCore.QRect(20, 80, 231, 20))
        self.labelAuthor.setText("")
        self.labelAuthor.setObjectName("labelAuthor")
        self.labelAuthorEmail = QtWidgets.QLabel(AboutForm)
        self.labelAuthorEmail.setGeometry(QtCore.QRect(20, 130, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelAuthorEmail.setFont(font)
        self.labelAuthorEmail.setText("")
        self.labelAuthorEmail.setObjectName("labelAuthorEmail")

        self.retranslateUi(AboutForm)
        QtCore.QMetaObject.connectSlotsByName(AboutForm)

    def retranslateUi(self, AboutForm):
        _translate = QtCore.QCoreApplication.translate
        AboutForm.setWindowTitle(_translate("AboutForm", "Form"))

