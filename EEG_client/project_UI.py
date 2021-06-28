import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QCoreApplication

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton("Get EEG", self)
        btn1.clicked.connect(self.clicked1)
        btn2 = QPushButton('Preprocess EEG', self)
        btn2.clicked.connect(self.clicked2)
        btn3 = QPushButton('Send EEG', self)
        btn3.clicked.connect(self.clicked3)

        btn4 = QPushButton('Ok', self)
        btn5 = QPushButton('Cancel', self)
        btn5.clicked.connect(QCoreApplication.instance().quit)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(btn1)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(btn2)
        
        hbox3 = QHBoxLayout()
        hbox3.addWidget(btn3)

        result = QLabel('Result', self)
        result.setAlignment(Qt.AlignCenter)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(result)
        
        hbox5 = QHBoxLayout()
        hbox5.addWidget(btn4)
        hbox5.addWidget(btn5)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)

        self.setLayout(vbox)
        
    def clicked1(self):
        QMessageBox.about(self, "message", "clicked1")
        #print(os.getcwd())
        os.system('D:\\ThinkGearData\\thinkgear_testapp\\Debug\\thinkgear_testapp.exe 60')

    def clicked2(self):
        QMessageBox.about(self, "message", "clicked2")
        os.system('D:\\ThinkGearData\\preprocess_artifact.py')

    def clicked3(self):
        QMessageBox.about(self, "message", "clicked3")
        os.system('D:\\ThinkGearData\\socket_client.py')
        #data = os.system('socket_client.py')
        


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        wg = MyApp()
        self.setCentralWidget(wg)

        self.setWindowTitle('JaeJu - Depression Detection')
        self.setWindowIcon(QIcon('.\\images\\jj.png'))
        #self.setGeometry(150, 150, 400, 300)   
        self.resize(400, 300)
        self.center()
        
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex2 = MyWindow()
    sys.exit(app.exec_())

    #ex.show()
    #app.exec_()
