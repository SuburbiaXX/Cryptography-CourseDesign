import sys
import os
import re

from MD5 import *
from MD5 import MD5
from RSA import *
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from RSA import *


# class GUI(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.resize(600, 800)
#         self.setWindowTitle('密码学实验')
#
#         self.desktop = QApplication.desktop()
#         self.screenRect = self.desktop.screenGeometry()
#         self.screenheight = self.screenRect.height()
#         self.screenwidth = self.screenRect.width()
#
#         print("Screen height {}".format(self.screenheight))
#         print("Screen width {}".format(self.screenwidth))
#
#         # 手动输入的文本框
#         self.textinput1 = QTextEdit(self)
#         self.textinput1.setGeometry(20, 20, 400, 80)
#         self.textinput1.setFont(QFont("Timers", 16))
#         self.textinput1.setPlaceholderText('请输入需要进行MD5的字符串')
#
#         # 手动输入执行
#         self.button1 = QPushButton('执行', self)
#         self.button1.setGeometry(430, 50, 160, 30)
#         self.button1.setFont(QFont("Timers", 14))
#         self.button1.clicked.connect(self.exec_text)
#
#         # 从文件中读取执行
#         self.button2 = QPushButton('从文件中读取', self)
#         self.button2.setGeometry(430, 100, 160, 30)
#         self.button2.setFont(QFont("Timers", 14))
#         self.button2.clicked.connect(self.exec_file)
#
#         # 文本框展示MD5结果
#         self.textBrowser1 = QTextBrowser(self)
#         self.textBrowser1.setGeometry(20, 130, 400, 80)
#         self.textBrowser1.setFont(QFont("Timers", 16))
#         self.textBrowser1.setPlaceholderText('进行MD5后的结果')
#
#         # RSA签名部分
#         self.Label1 = QLabel('RSA部分', self)
#         self.Label1.setGeometry(20, 230, 400, 30)
#         self.Label1.setFont(QFont("Timers", 14))
#
#         self.textinput2 = QTextEdit(self)
#         self.textinput2.setGeometry(20, 270, 400, 60)
#         self.textinput2.setFont(QFont("Timers", 16))
#         self.textinput2.setPlaceholderText('请输入构造RSA所希望的两个大素数的位数,随意隔开即可')
#
#         self.button3 = QPushButton('执行', self)
#         self.button3.setGeometry(430, 300, 160, 30)
#         self.button3.setFont(QFont("Timers", 14))
#         self.button3.clicked.connect(self.exec_rsa)
#
#         self.textBrowser2 = QTextBrowser(self)
#         self.textBrowser2.setGeometry(20, 350, 450, 150)
#         self.textBrowser2.setFont(QFont("Timers", 16))
#         self.textBrowser2.setPlaceholderText('使用的RSA签名系统情况\n对上述MD5进行签名的结果')
#
#     # 处理文件中获取的字符串，进行MD5后直接写入textBrowser1
#     def exec_file(self):
#         filename, _ = QFileDialog.getOpenFileName(self, 'Open File', './')
#
#         # 如果txt文件为空,则提示并返回
#         filesize = os.path.getsize(filename)
#         if filesize == 0:
#             QMessageBox.information(self, '提示', '请选择非空的txt文件')
#             return
#
#         mes = MD5(GetRawInfo_File(filename))
#         mes.fill_text()
#         result = mes.group_processing()
#         result = EncryptAES(result)  # 这一步添加AES操作
#
#         self.textBrowser1.setPlainText(result)
#
#     # 处理直接输入的字符串，进行MD5后直接写入textBrowser1
#     def exec_text(self):
#         text = self.textinput1.toPlainText()
#
#         # 如果输入为空,则提示并返回
#         if text == '':
#             QMessageBox.information(self, '提示', '请输入需要进行MD5算法字符串')
#             return
#
#         # print(text)
#         text = text.encode('utf-8')
#         # print(text)
#
#         mes = MD5(GetRawInfo_Text(text))
#         mes.fill_text()
#         result = mes.group_processing()
#         result = EncryptAES(result)  # 这一步添加AES操作
#         self.textBrowser1.setPlainText(result)
#
#     def exec_rsa(self):
#         text = self.textinput2.toPlainText()
#
#         # 如果输入为空,则提示并返回
#         if text == '':
#             QMessageBox.information(self, '提示', '请输入需要进行RSA算法的两个大素数的位数')
#             return
#
#         # 正则匹配字符串中的数字
#         pattern = re.compile(r'\d+')
#         temp = pattern.findall(text)
#         r = []
#         r.append(int(temp[0]))
#         r.append(int(temp[1]))
#         # print(result)
#         print(r)
#         if len(temp) != 2 | r[0] > 500 | r[1] > 500 | r[0] < 1 | r[1] < 1:
#             QMessageBox.information(self, '提示', '请输入正确的位数,注意位数超出100后生成较慢，故不建议过大')
#             return
#
#         # 生成公钥私钥
#         p, q = generate_prime(r[0], r[1])
#         n = p * q
#         phi = (p - 1) * (q - 1)
#         e, d = generate_key(phi)
#
#         result = "p = " + str(p) + "\nq = " + str(q) + "\nn = " + str(n) + "\ne = " + str(e) + "\nd = " + str(d)
#         self.textBrowser2.setPlainText(result)
#
#         # 读取MD5结果
#         if self.textBrowser1.toPlainText() == '':
#             QMessageBox.information(self, '提示', '请先进行MD5')
#             return
#
#         # 进行RSA签名
#         message = self.textBrowser1.toPlainText()
#         # 将字符串平均划分成4部分
#         mes = [message[i:i + 8] for i in range(0, len(message), 8)]  # 8个字符一组
#         print(mes)
#         # 将每一部分转换成十六进制
#         mes_hex = []
#         for i in range(len(mes)):
#             mes[i] = "0x" + mes[i]
#             mes_hex.append(int(mes[i], 16))
#
#         for i in range(len(mes_hex)):
#             mes_hex[i] = fast_power(mes_hex[i], d, n)
#         # 输出结果
#         result = "签名结果为：\n"
#         for i in range(len(mes_hex)):
#             result += str(hex(mes_hex[i])) + "\n"
#         self.textBrowser2.append(result)


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(753, 691)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setPlaceholderText("")
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_3.addWidget(self.textEdit)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_3.addWidget(self.textBrowser)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_4.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.horizontalLayout.addWidget(self.textBrowser_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setEnabled(True)
        self.pushButton_5.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_2.addWidget(self.pushButton_6)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 6, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayout_2.addWidget(self.textEdit_2)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.horizontalLayout_2.addWidget(self.textBrowser_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setEnabled(True)
        self.pushButton_7.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_3.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_3.addWidget(self.pushButton_8)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 4, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 5, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.textEdit, self.textBrowser)
        MainWindow.setTabOrder(self.textBrowser, self.pushButton)
        MainWindow.setTabOrder(self.pushButton, self.pushButton_2)
        MainWindow.setTabOrder(self.pushButton_2, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.textEdit_2)
        MainWindow.setTabOrder(self.textEdit_2, self.textBrowser_2)
        MainWindow.setTabOrder(self.textBrowser_2, self.pushButton_7)
        MainWindow.setTabOrder(self.pushButton_7, self.pushButton_8)
        MainWindow.setTabOrder(self.pushButton_8, self.textBrowser_3)
        MainWindow.setTabOrder(self.textBrowser_3, self.pushButton_5)
        MainWindow.setTabOrder(self.pushButton_5, self.pushButton_6)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "密码学课程设计实验"))
        self.textEdit.setFont(QFont("Timers", 14))
        self.textEdit.setPlaceholderText("请输入需要进行MD5操作的字符串")

        self.textBrowser.setFont(QFont("Timers", 14))
        self.textBrowser.setPlaceholderText("进行MD5操作后的结果")

        self.pushButton.setText(_translate("MainWindow", "执行MD5"))
        self.pushButton.setFont(QFont("Timers", 12))
        self.pushButton.clicked.connect(self.exec_text)
        self.pushButton.setFixedSize(120, 50)

        self.pushButton_2.setText(_translate("MainWindow", "选择txt文件"))
        self.pushButton_2.setFont(QFont("Timers", 12))
        self.pushButton_2.clicked.connect(self.exec_file)

        self.pushButton_3.setText(_translate("MainWindow", "清空1"))

        self.textBrowser_3.setFont(QFont("Timers", 14))
        self.textBrowser_3.setPlaceholderText("进行验证操作后的结果")

        self.pushButton_5.setText(_translate("MainWindow", "签名验证"))
        self.pushButton_5.setFixedSize(120, 50)
        self.pushButton_5.clicked.connect(self.exec_rsa_verify)
        self.pushButton_5.setFont(QFont("Timers", 12))
        self.pushButton_6.setText(_translate("MainWindow", "清空3"))

        self.textEdit_2.setFont(QFont("Timers", 14))
        self.textEdit_2.setPlaceholderText('请输入构造RSA所希望的两个大素数的位数,随意隔开即可')

        self.textBrowser_2.setFont(QFont("Timers", 14))
        self.textBrowser_2.setPlaceholderText('使用的RSA签名系统情况\n对上述MD5进行签名的结果')

        self.pushButton_7.setText(_translate("MainWindow", "进行消息签名"))
        self.pushButton_7.setFont(QFont("Timers", 12))
        self.pushButton_7.clicked.connect(self.exec_rsa_sign)

        self.pushButton_8.setText(_translate("MainWindow", "清空2"))
        self.pushButton_8.setFixedSize(120, 50)

    # 处理文件中获取的字符串，进行MD5后直接写入textBrowser
    def exec_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Text files(*.txt)')

        # 没选中文件，返回
        if filename == "":
            return
        # 如果txt文件为空,则提示并返回
        filesize = os.path.getsize(filename)
        if filesize == 0:
            QMessageBox.information(self, '提示', '请选择非空的txt文件')
            return

        mes = MD5(GetRawInfo_File(filename))
        mes.fill_text()
        result = mes.group_processing()
        result = EncryptAES(result)  # 这一步添加AES操作

        self.textBrowser.setPlainText(result)

    # 处理直接输入的字符串，进行MD5后直接写入textBrowser
    def exec_text(self):
        text = self.textEdit.toPlainText()
        # print(text)
        # 如果输入为空,则提示并返回
        if text == '':
            QMessageBox.information(self, '提示', '请输入需要进行MD5算法字符串')
            return

        # print(text)
        text = text.encode('utf-8')
        # print(text)

        mes = MD5(GetRawInfo_Text(text))
        mes.fill_text()
        result = mes.group_processing()
        result = EncryptAES(result)  # 这一步添加AES操作
        self.textBrowser.setPlainText(result)

    def exec_rsa_sign(self):
        text = self.textEdit_2.toPlainText()

        # 如果输入为空,则提示并返回
        if text == '':
            QMessageBox.information(self, '提示', '请输入需要进行RSA算法的两个大素数的位数')
            return

        # 读取MD5结果
        if self.textBrowser.toPlainText() == '':
            QMessageBox.information(self, '提示', '请先进行MD5')
            return

        # 正则匹配字符串中的数字
        pattern = re.compile(r'\d+')
        temp = pattern.findall(text)
        print(temp)
        r = []
        r.append(int(temp[0]))
        r.append(int(temp[1]))
        print(r)
        if len(temp) != 2 or r[0] > 200 or r[1] > 200 or r[0] < 1 or r[1] < 1 or r[0] + r[1] < 10 or abs(
                r[0] - r[1]) > 5:
            QMessageBox.information(self, '提示', '请输入正确的位数,注意位数超出200后生成较慢，故不建议过大'
                                                  '\n同时为了保证签名正确性,二者位数之和不要小于11'
                                                  '\n为了保证RSA的安全性,二者位数之差不要过大,建议不要大于5')
            return

        # 生成公钥私钥
        p, q = generate_prime(r[0], r[1])
        n = p * q
        phi = (p - 1) * (q - 1)
        e, d = generate_key(phi)

        result = "p = " + str(p) + "\nq = " + str(q) + "\nn = " + str(n) + "\ne = " + str(e) + "\nd = " + str(d)
        self.textBrowser_2.setPlainText(result)

        # 进行RSA签名
        message = self.textBrowser.toPlainText()
        # 将字符串平均划分成4部分
        mes = [message[i:i + 8] for i in range(0, len(message), 8)]  # 8个字符一组
        # print(mes)
        # 将每一部分转换成十六进制
        mes_hex = []
        for i in range(len(mes)):
            mes[i] = "0x" + mes[i]
            mes_hex.append(int(mes[i], 16))

        for i in range(len(mes_hex)):
            mes_hex[i] = fast_power(mes_hex[i], d, n)
        # 输出结果
        result = "签名结果为：\n"
        for i in range(len(mes_hex)):
            result += str(hex(mes_hex[i])) + "\n"
        self.textBrowser_2.append(result)

    def exec_rsa_verify(self):
        # 获取textBrowser_2中的内容
        text = self.textBrowser_2.toPlainText()
        if text == '':
            QMessageBox.information(self, '提示', '请先进行RSA签名')
            return
        # print(text)
        # 正则匹配字符串中的 'e = ' 和 'n = ' 后的数字
        pattern = re.compile(r'e = (\d+)')
        temp = pattern.findall(text)
        # print(temp)
        e = int(temp[0])
        print("e = " + str(e))

        pattern = re.compile(r'n = (\d+)')
        temp = pattern.findall(text)
        # print(temp)
        n = int(temp[0])
        print("n = " + str(n))
        # 正则匹配字符串中的签名结果
        pattern = re.compile(r'0x(\w+)')
        temp1 = pattern.findall(text)
        # print(temp1)
        # 将签名结果转换成十进制
        mes = []
        for i in range(len(temp1)):
            mes.append(int(temp1[i], 16))
        print(mes)

        for i in range(len(mes)):
            mes[i] = fast_power(mes[i], e, n)

        result = "使用公钥e = " + str(e) + "\n验证结果为：\n"
        for i in range(len(mes)):
            result += str(hex(mes[i])) + "\n"
        self.textBrowser_3.setPlainText(result)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = GUI()
#     window.show()
#     sys.exit(app.exec_())
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
