import sys
import os

from MD5 import *
from MD5 import MD5
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(600, 600)
        self.setWindowTitle('密码学实验')

        # 手动输入的文本框
        self.textinput = QTextEdit(self)
        self.textinput.setGeometry(20, 20, 400, 150)
        self.textinput.setFont(QFont("Timers", 16))
        self.textinput.setPlaceholderText('请输入需要进行MD5算法字符串')

        # 手动输入执行按钮
        self.button1 = QPushButton('执行', self)
        self.button1.setGeometry(430, 50, 160, 30)
        self.button1.setFont(QFont("Timers", 14))
        self.button1.clicked.connect(self.exec_text)

        # 从文件中读取执行按钮
        self.button2 = QPushButton('从文件中读取', self)
        self.button2.setGeometry(430, 100, 160, 30)
        self.button2.setFont(QFont("Timers", 14))
        self.button2.clicked.connect(self.exec_file)

        # 文本框展示运行结果
        self.textBrowser1 = QTextBrowser(self)
        self.textBrowser1.setGeometry(20, 200, 400, 150)
        self.textBrowser1.setFont(QFont("Timers", 16))
        self.textBrowser1.setPlaceholderText('MD5加密结果')

    # 处理文件中获取的字符串，进行MD5后直接写入textBrowser1
    def exec_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', './')

        # 如果txt文件为空,则提示并返回
        filesize = os.path.getsize(filename)
        if filesize == 0:
            QMessageBox.information(self, '提示', '请选择非空的txt文件')
            return

        mes = MD5(GetRawInfo_File(filename))
        mes.fill_text()
        result = mes.group_processing()

        self.textBrowser1.setPlainText(result)

    def exec_text(self):
        text = self.textinput.toPlainText()

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

        self.textBrowser1.setPlainText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
