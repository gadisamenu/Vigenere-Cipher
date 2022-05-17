import importlib.util
import subprocess
import sys


if importlib.util.find_spec("PyQt5.QtCore"):
    print(f"Package already installed")
else:
    try:
        permission = input("Do you what to install PyQt5(y/n)?")
        if permission.lower() == "y":
            subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                                   'PyQt5'])
            print("Installed PyQt5 successfully")
        sys.exit(0)
    except Exception:
        print("Failed installing PyQt5")
        sys.exit(0)

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from tithemius import Tirthmius


class MainWindow(QWidget):
    encryption_algo = Tirthmius()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setAcceptDrops(True)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.textfield = TextInOut(self)
        self.mainLayout.addWidget(self.textfield, 30)

        self.buttons = Buttons(self)
        self.mainLayout.addWidget(self.buttons, 1)

        self.setWindowTitle("Trithemius")
        self.setGeometry(150, 150, 900, 600)


class TextInOut(QWidget):
    def __init__(self, parent:None):
        QWidget.__init__(self, parent)
        self.vLayout = QHBoxLayout()
        self.vLayout.setSpacing(15)
        self.vLayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.vLayout)
        TextInOut.take = QPlainTextEdit()
        TextInOut.take.setPlaceholderText("Insert Text")
        TextInOut.take.setStyleSheet("""
            QWidget {
                border: 1px solid grey;
                border-radius: 10px;
                background-color: rgb(255, 255, 255);
                }
            """)
        TextInOut.out = QPlainTextEdit()
        TextInOut.out.setPlaceholderText("Result Area")
        TextInOut.out.setStyleSheet("""
                QWidget {
                    border: 1px solid grey;
                    border-radius: 10px;
                    background-color: rgb(255, 255, 255);
                    }
                """)
        self.vLayout.addWidget(TextInOut.take, 1)
        self.vLayout.addWidget(TextInOut.out, 1)



class Buttons(QWidget):
    def __init__(self, parent:None):
        QWidget.__init__(self, parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("key")
        self.label.width = 8
        self.key = QLineEdit()
        self.key.setPlaceholderText("key")
        self.encrypt_btn = QPushButton("Encrypt")
        self.encrypt_btn.clicked.connect(self.action_encrypt)
        self.decrypt_btn = QPushButton("Decrypt")
        self.decrypt_btn.clicked.connect(self.action_decrypt)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.key, 3)
        self.layout.addWidget(self.encrypt_btn, 2)
        self.layout.addWidget(self.decrypt_btn, 2)

    def action_encrypt(self):
        key = self.key.text()
        if not key:
            return
        MainWindow.encryption_algo.key = self.key.text()
        MainWindow.encryption_algo.set_block_size(key)
        out_put = MainWindow.encryption_algo.encrypt(TextInOut.take.toPlainText())
        TextInOut.out.setPlainText(out_put)

    def action_decrypt(self):
        key = self.key.text()
        if not key:
            return
        MainWindow.encryption_algo.key = self.key.text()
        MainWindow.encryption_algo.set_block_size(key)
        out_put = MainWindow.encryption_algo.decrypt(TextInOut.take.toPlainText())
        TextInOut.out.setPlainText(out_put)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit((app.exec_()))