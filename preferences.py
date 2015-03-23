# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui'
#
# Created: Sun Apr 06 09:52:37 2014
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 411)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(10, 40, 181, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.comboBox_6 = QtGui.QComboBox(Dialog)
        self.comboBox_6.setGeometry(QtCore.QRect(190, 40, 201, 22))
        self.comboBox_6.setObjectName(_fromUtf8("comboBox_6"))
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(10, 70, 181, 21))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.comboBox_7 = QtGui.QComboBox(Dialog)
        self.comboBox_7.setGeometry(QtCore.QRect(190, 70, 201, 22))
        self.comboBox_7.setObjectName(_fromUtf8("comboBox_7"))
        self.comboBox_8 = QtGui.QComboBox(Dialog)
        self.comboBox_8.setGeometry(QtCore.QRect(190, 180, 201, 22))
        self.comboBox_8.setObjectName(_fromUtf8("comboBox_8"))
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(10, 150, 181, 21))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.comboBox_9 = QtGui.QComboBox(Dialog)
        self.comboBox_9.setGeometry(QtCore.QRect(190, 150, 201, 22))
        self.comboBox_9.setObjectName(_fromUtf8("comboBox_9"))
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(10, 180, 181, 21))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(10, 120, 381, 20))
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(10, 10, 381, 20))
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 230, 381, 171))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.comboBox_2 = QtGui.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(180, 50, 191, 22))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_3 = QtGui.QComboBox(self.groupBox)
        self.comboBox_3.setGeometry(QtCore.QRect(180, 80, 191, 22))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 20, 181, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 181, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(180, 20, 191, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox_5 = QtGui.QComboBox(self.groupBox)
        self.comboBox_5.setGeometry(QtCore.QRect(180, 140, 191, 22))
        self.comboBox_5.setObjectName(_fromUtf8("comboBox_5"))
        self.comboBox_4 = QtGui.QComboBox(self.groupBox)
        self.comboBox_4.setGeometry(QtCore.QRect(180, 110, 191, 22))
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 181, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 181, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 181, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_8.setText(_translate("Dialog", "Apply Filter to Tree View", None))
        self.label_9.setText(_translate("Dialog", "Apply Filter to Text Browser", None))
        self.label_10.setText(_translate("Dialog", "Apply Selection to Display", None))
        self.label_12.setText(_translate("Dialog", "Expand Collapse Element(s)", None))
        self.label_7.setText(_translate("Dialog", "--- Tree View -----------------------------------------------------------------------------", None))
        self.label_11.setText(_translate("Dialog", "--- Filter ----------------------------------------------------------------------------------", None))
        self.groupBox.setTitle(_translate("Dialog", "Colors", None))
        self.label.setText(_translate("Dialog", "Filter Match Elements", None))
        self.label_3.setText(_translate("Dialog", "Children of Match Elements", None))
        self.label_5.setText(_translate("Dialog", "Element Attributes", None))
        self.label_4.setText(_translate("Dialog", "Element and Attribute Data", None))
        self.label_2.setText(_translate("Dialog", "Parents of Match Elements", None))

