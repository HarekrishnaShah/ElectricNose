from PyQt5.QtWidgets import (QDialog, QApplication, QTableWidgetItem, QAbstractItemView, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTime, QTimer, QDir,QFile,QIODevice,QTextStream, pyqtSlot
from PyQt5.QtGui import QFont, QBrush, QIcon
from enum import Enum
import xlwt
import pandas as pd
from ui_analysisDialog import Ui_Dialog
from myClassifier import QmyClassifier

class CellType(Enum):    ##各单元格的类型
    ctToltime = 1000
    ctMaxtime = 1001
    ctMaxnum =1002
    ctMaxgrad = 1003
    ctMinnum = 1004
    ctMingrad = 1005
    ctRestime = 1006
    ctFormsize = 1007
    ctLatesize = 1008

class QmyAnalysis(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

        self.df = pd.DataFrame()

        # 保存按钮
        self.ui.saveButton.clicked.connect(self.data_save)
        self.ui.analysisButton.clicked.connect(self.data_analysis)
    
    def setInit(self, tolTime, maxTime, maxNum, minNum, firstNum, difNum, minTime):
        rowCount = self.ui.tableWidget.rowCount() #表格行数
        self.__createItemsARow(rowCount, tolTime, maxTime, maxNum, firstNum, minNum, difNum, minTime, 1, 1)
        
        data_tol = [[tolTime] * rowCount, maxTime.tolist(), maxNum.tolist(), firstNum, minNum.tolist(), difNum, minTime.tolist(), [1] * rowCount, [1] * rowCount]
        data_tol = [[row[i] for row in data_tol] for i in range(len(data_tol[0]))]
        self.df = pd.DataFrame(data_tol, columns=['ReactionTime', 'MaxLoc', 'Max', 'Origin', 'Min', 'Inte', 'MinLoc', 'Loc', 'None3']) 


    def __createItemsARow(self, rowCount, tolTime, maxTime, maxNum, firstNum, minNum, difNum, minTime, formSize, lateSize):
        for i in range(0, rowCount):
            item = QTableWidgetItem(str(tolTime), CellType.ctToltime.value)
            self.ui.tableWidget.setItem(i, 0, item)

            item = QTableWidgetItem(str(maxTime[i]), CellType.ctMaxtime.value)
            self.ui.tableWidget.setItem(i, 1, item)

            item = QTableWidgetItem(str(maxNum[i]), CellType.ctMaxnum.value)
            self.ui.tableWidget.setItem(i, 2, item)

            item = QTableWidgetItem(str(firstNum[i]), CellType.ctMaxgrad.value) 
            self.ui.tableWidget.setItem(i, 3, item)

            item = QTableWidgetItem(str(minNum[i]), CellType.ctMinnum.value)
            self.ui.tableWidget.setItem(i, 4, item)

            item = QTableWidgetItem(str(difNum[i]), CellType.ctMingrad.value) 
            self.ui.tableWidget.setItem(i, 5, item)

            item = QTableWidgetItem(str(minTime[i]), CellType.ctRestime.value) 
            self.ui.tableWidget.setItem(i, 6, item)

            item = QTableWidgetItem(str(formSize), CellType.ctFormsize.value) #没写好
            self.ui.tableWidget.setItem(i, 7, item)

            item = QTableWidgetItem(str(lateSize), CellType.ctLatesize.value) #没写好
            self.ui.tableWidget.setItem(i, 8, item)
    
    # 保存数据
    def data_save(self):
        curPath=QDir.currentPath()    #获取系统当前目录
        title="另存为一个文件"        #对话框标题
        filt=".xls(*.xls)"  #文件过滤器
        fileName,flt=QFileDialog.getSaveFileName(self,title,curPath,filt)
        if (fileName==""):
            return
        if self.__saveByIODevice(fileName):
            return 
        else:
            QMessageBox.critical(self,"错误","保存文件失败")    

    #用QFile保存文件
    def __saveByIODevice(self,fileName):  
        wbk = xlwt.Workbook()
        self.sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        for col in range(self.ui.tableWidget.columnCount()):
            for row in range(self.ui.tableWidget.rowCount()):
                try:
                    text = str(self.ui.tableWidget.item(row, col).text())
                    self.sheet.write(row, col, text)
                except AttributeError:
                    pass
        
        wbk.save(fileName)
        return True
    
    #分析数据
    def data_analysis(self):
        classifierDialog = QmyClassifier()
        classifierDialog.setInit(self.df)
        classifierDialog.exec()



