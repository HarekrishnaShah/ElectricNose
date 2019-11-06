import sys
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import re
import res_rc
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow,QActionGroup,
                 QLabel, QProgressBar, QSpinBox, QFontComboBox, QMessageBox, QFileDialog, QDialog)
from PyQt5.QtCore import   QTime, QTimer, QDir,QFile,QIODevice,QTextStream, pyqtSlot
from ui_mainwindow import Ui_MainWindow
from mySerSetting import QmySerSetting

class GasManage(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)    #调用父类构造函数，创建窗体
        self.ui=Ui_MainWindow()     #创建UI对象
        self.ui.setupUi(self)       #构造UI界面
        self.__buildUI()    #动态创建组件，添加到工具栏和状态栏

        self.ser = serial.Serial()  
        self.port_check()           #检测所有存在的串口

        # 接收数据数目置零
        self.data_num_received = 0
        self.data_num_received_single = 0
        self.ui.recordEdit.setText(str(self.data_num_received))

        # 用来存储开始读取时的目标读取次数
        self.strNum = 0


        # 默认的串口数据
        self.portNum = 'COM5'
        self.portBaudrate = '9600'
        self.portBytesize = '8'
        self.portParity = 'N'
        self.portStopbits = '1'

        self.ui.stopButton.setEnabled(False)
        self.ui.startButton.setEnabled(False)
        self.ui.reButton.setEnabled(False)

        self.setFixedSize(self.width(), self.height()) # 禁止窗口拉伸 
        self.init()

    def init(self):
        # 打开串口按钮
        self.ui.openButton.clicked.connect(self.open_serial)

        # 关闭串口按钮
        self.ui.stopButton.clicked.connect(self.record_stop)

        # 开始读取按钮
        self.ui.startButton.clicked.connect(self.record_start)

        # 清除按钮
        self.ui.clearButton.clicked.connect(self.data_clear)

        # 保存按钮
        self.ui.saveButton.clicked.connect(self.data_save)

        # 重置按钮
        self.ui.reButton.clicked.connect(self.refresh)

        # 绘图按钮
        self.ui.drawButton.clicked.connect(self.initPlot)


        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)

    def __buildUI(self):    ##窗体上动态添加组件
        # 创建状态栏上的组件
        self.__LabFile=QLabel(self)     # QLabel组件显示信息
        self.__LabFile.setMinimumWidth(200)
        self.ui.statusbar.addWidget(self.__LabFile)
        self.__LabFile.setText("串口未打开")



        self.__progressBar1=QProgressBar(self)      # progressBar1
        self.__progressBar1.setMaximumWidth(200)
        self.__progressBar1.setMinimum(0)
        self.__progressBar1.setMaximum(2000)
        self.ui.statusbar.addWidget(self.__progressBar1)

    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
        if len(self.Com_Dict) == 0:
            self.ui.stateEdit.setText("未搜索到串口")
        else:
            self.ui.stateEdit.setText("已搜索到串口")
    
    # 打开串口
    def open_serial(self):
        self.ser.port = self.portNum
        self.ser.baudrate = int(self.portBaudrate)
        self.ser.bytesize = int(self.portBytesize)
        self.ser.stopbits = int(self.portStopbits)
        self.ser.parity = self.portParity
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)
        time.sleep(1) #给一点延时，防止冲突
        

        if self.ser.isOpen():
            self.ui.stopButton.setEnabled(True)
            self.ui.startButton.setEnabled(True)
            self.ui.reButton.setEnabled(True)
            self.ui.openButton.setEnabled(False)
            self.__LabFile.setText("成功打开串口")

    # 开始录入
    def record_start(self):
        if self.ser.isOpen():
            self.__LabFile.setText("正在录入")
            input_s = int(self.ui.readnumBox.currentText())
            self.strNum = input_s
            if input_s != "":
                input_s = (str(input_s) + '\r').encode('utf-8')
                self.ser.write(input_s)
                
        else:
            pass   
              
    # 关闭串口
    def record_stop(self):
        self.timer.stop()
        try:
            self.ser.close()
        except:
            pass

        if ~self.ser.isOpen():
            self.ui.stopButton.setEnabled(False)
            self.ui.startButton.setEnabled(False)
            self.ui.reButton.setEnabled(False)
            self.ui.openButton.setEnabled(True)
            self.__LabFile.setText("成功关闭串口")
    
    # 重置按钮
    def refresh(self):
        # 重置步骤：1、关闭串口，将各个按钮状态恢复到初始状态
        self.record_stop()
        self.ui.stopButton.setEnabled(False)
        self.ui.startButton.setEnabled(False)
        self.ui.reButton.setEnabled(False)
        self.ui.openButton.setEnabled(True)

        # 2、数值清零，状态栏复原
        self.data_num_received = 0
        self.data_num_received_single = 0
        self.strNum = 0
        self.__LabFile.clear()
        self.__progressBar1.setValue(0)

        # 3、文本框清空
        self.ui.receiveText.clear()

        # 4、串口状态栏重置
        self.ui.recordEdit.setText('0')
        self.port_check()           #检测所有存在的串口

    # 接收数据
    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.record_stop()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            
            self.ui.receiveText.insertPlainText(data.decode('utf-8'))

            # 获取到text光标
            textCursor = self.ui.receiveText.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.ui.receiveText.setTextCursor(textCursor)

            # 如果检测到本串数据的截止
            if data.decode('utf-8').find('\r') != -1:
                # 增加读取到的数量显示
                self.data_num_received += 1
                self.data_num_received_single += 1
                self.ui.recordEdit.setText(str(self.data_num_received))   
                sz = 2000 * (self.data_num_received_single / self.strNum)
                self.__progressBar1.setValue(sz)

                if self.data_num_received_single == self.strNum:
                    self.data_num_received_single = 0
                    self.__LabFile.setText("接收完毕")

                    #开始绘图
                    if self.ui.drawBox.isChecked():
                        self.initPlot()

        else:
            pass
    
    # 清除接收窗口
    def data_clear(self):
        self.ui.receiveText.clear()
        self.__LabFile.setText("接收窗口已清除")

    # 保存数据
    def data_save(self):
        curPath=QDir.currentPath()    #获取系统当前目录
        title="另存为一个文件"        #对话框标题
        filt="文本文件(*.txt)"  #文件过滤器
        fileName,flt=QFileDialog.getSaveFileName(self,title,curPath,filt)
        if (fileName==""):
            return
        if self.__saveByIODevice(fileName):
            self.__LabFile.setText("文件名： " + fileName)
        else:
            QMessageBox.critical(self,"错误","保存文件失败")    

    #用QFile保存文件
    def __saveByIODevice(self,fileName):  
        fileDevice=QFile(fileName)
        if not fileDevice.open(QIODevice.WriteOnly | QIODevice.Text):
            return False
        try:
            text = self.ui.receiveText.toPlainText()
            strBytes=text.encode("utf-8")        # str转换为bytes类型
            fileDevice.write(strBytes)           #写入文件
        finally:
            fileDevice.close()
        return  True    
    
    # 初始化绘图
    def initPlot(self):
        plt.figure(1)
        plt.title("Gas curve")
        plt.xlabel("Times")
        plt.ylabel("Sensor Value")
        plt.grid(True) # 添加网格

        # 图表纵轴
        y = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

        # 处理字符串
        text = self.ui.receiveText.toPlainText()
        result = re.findall(r'\d* ', text)
        result = list(map(int, result))

        for i in range(int(len(result) / 15)):
            for j in range(15):
                y[j].append(result[i * 15 + j])

        x = range(len(y[0]))

        plt.plot(x, y[0], x, y[1], x, y[2], x, y[3], x, y[4], x, y[5], x, y[6], x, y[7], x, y[8], x, y[9], x, y[10], x, y[11], x, y[12], x, y[13], x, y[14])
        plt.show()

    # 编辑串口
    @pyqtSlot()
    def on_actSer_triggered(self):
        settingDialog = QmySerSetting()  
        settingDialog.setInit(self.portNum, self.portBaudrate, self.portBytesize, self.portStopbits)
        ret = settingDialog.exec()
        if (ret == QDialog.Accepted):
            self.portNum, self.portBaudrate, self.portBytesize, self.portStopbits = settingDialog.getSer()
            #print(self.portNum + self.portBaudrate + self.portBytesize + self.portStopbits)

    # 关于系统        
    @pyqtSlot()
    def on_actAboutSys_triggered(self):
        dlgTitle = "About System"
        strInfo = "得康科技有限公司研发\n保留所有版权"
        QMessageBox.about(self, dlgTitle, strInfo)

    # 关于Qt     
    @pyqtSlot()
    def on_actAboutQt_triggered(self):
        dlgTitle="About Qt"
        QMessageBox.aboutQt(self, dlgTitle)


if __name__ == '__main__':
    app = QApplication(sys.argv)    #创建GUI应用程序
    form=GasManage()            #创建窗体
    form.show()
    sys.exit(app.exec_())
