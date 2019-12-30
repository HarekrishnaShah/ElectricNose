# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 173)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(9, 9, 261, 121))
        self.groupBox.setObjectName("groupBox")
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setGeometry(QtCore.QRect(10, 30, 81, 71))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.splitter)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setObjectName("label_2")
        self.splitter_2 = QtWidgets.QSplitter(self.groupBox)
        self.splitter_2.setGeometry(QtCore.QRect(100, 30, 141, 71))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.sexEdit = QtWidgets.QLineEdit(self.splitter_2)
        self.sexEdit.setReadOnly(True)
        self.sexEdit.setObjectName("sexEdit")
        self.ageEdit = QtWidgets.QLineEdit(self.splitter_2)
        self.ageEdit.setReadOnly(True)
        self.ageEdit.setObjectName("ageEdit")
        self.bodyEdit = QtWidgets.QLineEdit(self.splitter_2)
        self.bodyEdit.setReadOnly(True)
        self.bodyEdit.setObjectName("bodyEdit")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 54, 12))
        self.label_4.setObjectName("label_4")
        self.selectedEdit = QtWidgets.QLineEdit(Dialog)
        self.selectedEdit.setGeometry(QtCore.QRect(110, 140, 141, 20))
        self.selectedEdit.setReadOnly(True)
        self.selectedEdit.setObjectName("selectedEdit")
        self.selectButton = QtWidgets.QPushButton(Dialog)
        self.selectButton.setGeometry(QtCore.QRect(290, 20, 75, 23))
        self.selectButton.setObjectName("selectButton")
        self.analysisButton = QtWidgets.QPushButton(Dialog)
        self.analysisButton.setGeometry(QtCore.QRect(290, 60, 75, 23))
        self.analysisButton.setObjectName("analysisButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "数据分析"))
        self.groupBox.setTitle(_translate("Dialog", "响应结果"))
        self.label.setText(_translate("Dialog", "性别："))
        self.label_3.setText(_translate("Dialog", "年龄段："))
        self.label_2.setText(_translate("Dialog", "身体状态："))
        self.label_4.setText(_translate("Dialog", "Selected："))
        self.selectButton.setText(_translate("Dialog", "选择分类器"))
        self.analysisButton.setText(_translate("Dialog", "分析"))

