#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Boyce Chen
@Date   ：2020-03-22 19:26
@Desc   ：
=================================================="""
import time
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QmessageBox
from TimeConversion1 import Ui_TimeFormatConvert

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ';' + os.environ['PATH']


class myMainWindows(QMainWindow, Ui_TimeFormatConvert):
    def __init__(self, parent=None):
        super(myMainWindows, self).__init__(parent)
        self.setupUi(self)
        # 获取当前标准格式的时间，并默认填入
        self.StandartTimeEdit.setText(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.errorMsg = {'DataErr': 'Data input error, please check again.',
                         'RBtnCheckErr': "please choose a Radio Button.",
                         }
        self.ConvertBtn.clicked.connect(self.ConvertClick)  # 点击按钮绑定事件
        self.StandardTime_radioBt.toggled.connect(self.btnstate)  # 单选框触发信号
        self.UnixTime_radioBt.toggled.connect(self.btnstate)  # 单选框触发信号

    # 检查单选按钮状态吗，并保持互斥行为
    def btnstate(self):
        if self.StandardTime_radioBt.ischecked():
            self.UnixTimeEdit.setReadOnly(True)
            self.StandardTimeEdit.setReadOnly(False)
        if self.UnixTime_radioBt.ischecked():
            self.UnixTimeEdit.setReadOnly(False)
            self.StandardTimeEdit.setReadOnly(True)

    # Unix时间转换成标准时间
    def unix2normal(self, unix_time):
        unix_time = int(unix_time) * 1000
        timeArray = time.localtime(unix_time)
        normal_time = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)

        self.StandardTimeEdit.clear()
        self.StandardTimeEdit.setText(str(normal_time))

    # 标准时间转换成unix时间
    def normal2unix(self, standart_time):
        try:
            timeArray = time.strptime(standart_time, "%Y-%m-%d %H:%M:%S")
            unixTime = int(time.mktime(timeArray))
            unixTime *= 1000

            self.UnixTimeEdit.clear()
            self.UnixTimeEdit.setText(str(unixTime))
        except Exception as e:
            QmessageBox.warning(self, 'ERROR', self.errorMsg.get('DataErr') + '\n' + str(e), QmessageBox.Ok)

    # 判断输入内容是否合法
    def textCheck(self, unixTime):
        if unixTime.isdigit() and 14 >= len(unixTime):
            return True
        else:
            return False

    # 转换按钮点击事件
    def ConvertClick(self):
        self.unixTime = self.UnixTimeEdit.text()
        self.standardTime = self.UnixTimeEdit.text()  # 获取文本框内容

        if self.StandardTime_radioBt.ischecked():  # 标准时间单选框被选择
            self.normal2unix(self.standardTime)

        elif self.UnixtTime_radioBt.ischecked():  # unix时间单选框被选择
            if self.textCheck(self.unixTime) is True:  # 判断unix时间输入是否合法
                self.unix2normal(self.unixTime)
            else:
                QmessageBox.warning(self, 'ERROR', self.errorMsg.get('DataErr'), QmessageBox.Ok)
        else:
            QmessageBox.information(self, 'Tips', self.errorMsg.get('RBtnCheckErr'), QmessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = myMainWindows()
    ui = Ui_TimeFormatConvert()
    myWin.show()
    sys.exit(app.exec_())
