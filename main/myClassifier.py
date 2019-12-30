from PyQt5.QtWidgets import (QDialog, QApplication, QTableWidgetItem, QAbstractItemView, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTime, QTimer, QDir,QFile,QIODevice,QTextStream, pyqtSlot
from PyQt5.QtGui import QFont, QBrush, QIcon
from ui_classifierDialog import Ui_Dialog
import pandas as pd
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class QmyClassifier(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

        self.ui.selectButton.clicked.connect(self.selectClassifier)
        self.ui.analysisButton.clicked.connect(self.analysis)

        

        self.data_ones = pd.DataFrame()
        self.new_clf = 0
    
    def setInit(self, data_tol):
        for i in range(15):
            if abs(data_tol.iloc[i, 2] - data_tol.iloc[i, 3]) > abs(data_tol.iloc[i, 4] - data_tol.iloc[i, 3]):#如果曲线是上升趋势
                data_tol.iloc[i, 7] = data_tol.iloc[i, 1]
            else:
                data_tol.iloc[i, 7] = data_tol.iloc[i, 6]
        
        data_xls_all = pd.concat([data_tol['Max'], data_tol['Origin'], data_tol['Min'], data_tol['Loc']])
        s = data_xls_all.values

        data = {'Max_0':[s[0]], 'Max_1':[s[1]], 'Max_2':[s[2]], 'Max_3':[s[3]], 'Max_4':[s[4]], 'Max_5':[s[5]], 'Max_6':[s[6]], 'Max_7':[s[7]], 'Max_8':[s[8]], 'Max_9':[s[9]], 'Max_10':[s[10]], 'Max_11':[s[11]], 'Max_12':[s[12]], 'Max_13':[s[13]], 'Max_14':[s[14]],\
    'Origin_0':[s[15]], 'Origin_1':[s[16]], 'Origin_2':[s[17]], 'Origin_3':[s[18]], 'Origin_4':[s[19]], 'Origin_5':[s[20]], 'Origin_6':[s[21]], 'Origin_7':[s[22]], 'Origin_8':[s[23]], 'Origin_9':[s[24]], 'Origin_10':[s[25]], 'Origin_11':[s[26]], 'Origin_12':[s[27]], 'Origin_13':[s[28]], 'Origin_14':[s[29]],\
        'Min_0':[s[30]], 'Min_1':[s[31]], 'Min_2':[s[32]], 'Min_3':[s[33]], 'Min_4':[s[34]], 'Min_5':[s[35]], 'Min_6':[s[36]], 'Min_7':[s[37]], 'Min_8':[s[38]], 'Min_9':[s[39]], 'Min_10':[s[40]], 'Min_11':[s[41]], 'Min_12':[s[42]], 'Min_13':[s[43]], 'Min_14':[s[44]],\
            'Loc_0':[s[45]], 'Loc_1':[s[46]], 'Loc_2':[s[47]], 'Loc_3':[s[48]], 'Loc_4':[s[49]], 'Loc_5':[s[50]], 'Loc_6':[s[51]], 'Loc_7':[s[52]], 'Loc_8':[s[53]], 'Loc_9':[s[54]], 'Loc_10':[s[55]], 'Loc_11':[s[56]], 'Loc_12':[s[57]], 'Loc_13':[s[58]], 'Loc_14':[s[59]]}

        
        #data = pd.DataFrame(data_xls_all.values)

        data = pd.DataFrame(data)

        for i in range(15):#对15个传感器的数据做平移处理
            s1 = 'Max_' + str(i)
            s2 = 'Origin_' + str(i)
            s3 = 'Min_' + str(i)

            data[s1] = data[s1] - data[s2]
            data[s3] = data[s3] - data[s2]

            data.drop(s2, axis = 1, inplace = True)#axis = 1表示列

        self.data_ones = data
        print(data)
    
    # 选择分类器
    def selectClassifier(self):
        curPath = QDir.currentPath()
        title = "选择一个分类器"
        filt = "程序文件(*.h *.cpp *.py *.m);;文本文件(*.txt);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        self.ui.selectedEdit.setText(fileName)

        self.new_clf = joblib.load(fileName)
    
    def analysis(self):
        if self.new_clf:
            res = self.new_clf.predict(self.data_ones)

            if res == 'male':
                self.ui.sexEdit.setText("男性")
            else:
                self.ui.sexEdit.setText("女性")

        else:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")




        
        

        


    


