import sys
import os
import re

from MD5 import *
from MD5 import MD5
from RSA import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(600, 800)
        self.setWindowTitle('密码学实验')

        # 手动输入的文本框
        self.textinput1 = QTextEdit(self)
        self.textinput1.setGeometry(20, 20, 400, 80)
        self.textinput1.setFont(QFont("Timers", 16))
        self.textinput1.setPlaceholderText('请输入需要进行MD5的字符串')

        # 手动输入执行
        self.button1 = QPushButton('执行', self)
        self.button1.setGeometry(430, 50, 160, 30)
        self.button1.setFont(QFont("Timers", 14))
        self.button1.clicked.connect(self.exec_text)

        # 从文件中读取执行
        self.button2 = QPushButton('从文件中读取', self)
        self.button2.setGeometry(430, 100, 160, 30)
        self.button2.setFont(QFont("Timers", 14))
        self.button2.clicked.connect(self.exec_file)

        # 文本框展示MD5结果
        self.textBrowser1 = QTextBrowser(self)
        self.textBrowser1.setGeometry(20, 130, 400, 80)
        self.textBrowser1.setFont(QFont("Timers", 16))
        self.textBrowser1.setPlaceholderText('进行MD5后的结果')

        # RSA签名部分
        self.Label1 = QLabel('RSA部分', self)
        self.Label1.setGeometry(20, 230, 400, 30)
        self.Label1.setFont(QFont("Timers", 14))

        self.textinput2 = QTextEdit(self)
        self.textinput2.setGeometry(20, 270, 400, 60)
        self.textinput2.setFont(QFont("Timers", 16))
        self.textinput2.setPlaceholderText('请输入构造RSA所希望的两个大素数的位数,随意隔开即可')

        self.button3 = QPushButton('执行', self)
        self.button3.setGeometry(430, 300, 160, 30)
        self.button3.setFont(QFont("Timers", 14))
        self.button3.clicked.connect(self.exec_rsa)

        self.textBrowser2 = QTextBrowser(self)
        self.textBrowser2.setGeometry(20, 350, 450, 150)
        self.textBrowser2.setFont(QFont("Timers", 16))
        self.textBrowser2.setPlaceholderText('使用的RSA签名系统情况\n对上述MD5进行签名的结果')

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

    # 处理直接输入的字符串，进行MD5后直接写入textBrowser1
    def exec_text(self):
        text = self.textinput1.toPlainText()

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

    def exec_rsa(self):
        text = self.textinput2.toPlainText()

        # 如果输入为空,则提示并返回
        if text == '':
            QMessageBox.information(self, '提示', '请输入需要进行RSA算法的两个大素数的位数')
            return

        # 正则匹配字符串中的数字
        pattern = re.compile(r'\d+')
        temp = pattern.findall(text)
        r = []
        r.append(int(temp[0]))
        r.append(int(temp[1]))
        # print(result)
        print(r)
        if len(temp) != 2 | r[0] > 500 | r[1] > 500 | r[0] < 1 | r[1] < 1:
            QMessageBox.information(self, '提示', '请输入正确的位数,注意位数超出100后生成较慢，故不建议过大')
            return

        # 生成公钥私钥
        p, q = generate_prime(r[0], r[1])
        n = p * q
        phi = (p - 1) * (q - 1)
        e, d = generate_key(phi)

        result = "p = " + str(p) + "\nq = " + str(q) + "\nn = " + str(n) + "\ne = " + str(e) + "\nd = " + str(d)
        self.textBrowser2.setPlainText(result)

        # 读取MD5结果
        if self.textBrowser1.toPlainText() == '':
            QMessageBox.information(self, '提示', '请先进行MD5')
            return

        # 进行RSA签名
        message = self.textBrowser1.toPlainText()
        # 将字符串平均划分成4部分
        mes = [message[i:i + 8] for i in range(0, len(message), 8)]  # 8个字符一组
        print(mes)
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
        self.textBrowser2.append(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
