from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from ui_QSerSetting import Ui_Dialog
import serial
import serial.tools.list_ports

class QmySerSetting(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.ui.serBox.currentTextChanged.connect(self.port_imf)
        self.port_check()

    def setInit(self, portNum, portBaudrate, portBytesize, portStopbits):
        self.ui.baudBox.setCurrentText(portBaudrate)
        self.ui.byteBox.setCurrentText(portBytesize)
        self.ui.stopBox.setCurrentText(portStopbits)

    
    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.ui.serBox.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.ui.serBox.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.state_label.setText(" 无串口")
    
    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.ui.serBox.currentText()
        if imf_s != "":
            self.ui.serLab.setText(self.Com_Dict[self.ui.serBox.currentText()])
            
    # 返回参数
    def getSer(self):
        portNum = self.ui.serBox.currentText() 
        portBaudrate = self.ui.baudBox.currentText()  
        portBytesize = self.ui.byteBox.currentText() 
        portStopbits = self.ui.stopBox.currentText() 

        return portNum, portBaudrate, portBytesize, portStopbits
