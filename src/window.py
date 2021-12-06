# -*- coding: utf-8 -*-

from os import truncate
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_main import Ui_MainWindow
from magic3api import magic3
from voiceapi import AiPlat

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.Widget)
        self.setWindowIcon(QtGui.QIcon('./img/favicon.ico'))
        #是否置顶flag
        self.__istop = False
        #是否开启语音提示
        self.__isVoice = True
        #结果状态
        self.__isOutput = False
        #绑定函数
        self.button_submit.clicked.connect(self.display)
        self.button_top.clicked.connect(self.setTopStatus)
        self.button_voiceStatus.clicked.connect(self.setVoiceStatus)
        self.button_reset.clicked.connect(self.ResetStatus)

        #其他接口
        self.__magic3 = magic3()
        self.__voice = AiPlat()

        #样式
        self.__stylenormal = ''
        self.__styleout = 'background:yellow'

    def ResetStatus(self):
        '''
        重置按钮
        '''
        text = [
            self.text00, self.text01, self.text02, self.text03, self.text04,
            self.text05, self.text06, self.text07, self.text08
        ]
        for i in range(0, 9):
            text[i].setText('')
            text[i].setReadOnly(False)
            text[i].setStyleSheet(self.__stylenormal)
        self.output.setText('')
        self.__isOutput = False

    def setVoiceStatus(self):
        '''
        方法：设置语音提示开启状态
        '''
        if self.__isVoice:
            #关闭语音
            self.__isVoice = False
            self.button_voiceStatus.setText('提示音：关')
        else:
            #开启语音
            self.__isVoice = True
            self.button_voiceStatus.setText('提示音：开')

    def setTopStatus(self):
        '''
        方法：置顶按钮处理方法
        '''
        if self.__istop:
            #取消置顶
            self.__istop = False
            self.button_top.setText('置頂')
            self.setWindowFlags(QtCore.Qt.Widget)
            self.show()
        else:
            #设置置顶
            self.__istop = True
            self.button_top.setText('取消置頂')
            self.setWindowFlags(QtCore.Qt.Widget
                                | QtCore.Qt.WindowStaysOnTopHint)
            self.show()

    def display(self):
        #计算处理函数
        if self.__isOutput:
            return
        text = [
            self.text00, self.text01, self.text02, self.text03, self.text04,
            self.text05, self.text06, self.text07, self.text08
        ]
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 9):
            if text[i].text() != '':
                data[i] = int(text[i].text())
        req = self.__magic3.getlist(data)
        outstring = '攻击顺序为：'
        if req['code'] == '0':
            self.__isOutput = True
            for i in range(0, 9):
                text[i].setText(str(req['data'][i]))
                text[i].setReadOnly(True)
                if i in req['index']:
                    text[i].setStyleSheet(self.__styleout)
                    outstring += str(req['data'][i]) + ','
            outstring = outstring.rstrip(',')
            self.output.setText(outstring)
            #获取声音
            if self.__isVoice:
                self.__voice.getVoice(outstring)
                self.__voice.playVoice()
        else:
            self.output.setText('计算出错，请检查数字')


if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
