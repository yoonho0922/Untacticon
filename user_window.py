import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton,QVBoxLayout,QLabel,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt



class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        neutral=QPixmap('public/neutral.png')

        lbl_img=QLabel()
        lbl_img.setPixmap(neutral)

        btn=QPushButton(self)
        btn.setIcon(QIcon('public/question_button.png'))
        btn.setCheckable(True)
        btn.clicked.connect(self.btn_clicked)

        btn.resize(300,50)

        vbox=QVBoxLayout()
        hbox=QHBoxLayout()

        hbox.addWidget(btn)

        vbox.addWidget(lbl_img)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle('user window')
        self.resize(200,300)
        self.center()
        self.show()

    def btn_clicked(self):
        QMessageBox.about(self,"message","Student 질문!")

    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MyApp()
    sys.exit(app.exec_())
