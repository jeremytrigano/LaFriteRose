# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/AELION/AppData/Local/Temp/lfr_centreqoGqKZ.ui',
# licensing of 'C:/Users/AELION/AppData/Local/Temp/lfr_centreqoGqKZ.ui' applies.
#
# Created: Sat Aug 10 12:15:12 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 621)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 239, 1001, 371))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 1001, 221))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.teDescr = QtWidgets.QTextEdit(self.widget)
        self.teDescr.setReadOnly(True)
        self.teDescr.setObjectName("teDescr")
        self.horizontalLayout.addWidget(self.teDescr)
        self.teAnim = QtWidgets.QTextEdit(self.widget)
        self.teAnim.setReadOnly(True)
        self.teAnim.setObjectName("teAnim")
        self.horizontalLayout.addWidget(self.teAnim)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Descriptif du centre", None, -1))

