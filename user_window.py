import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton,QVBoxLayout,QLabel,QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
from PyQt5.QtCore import *



class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.neutral=QPixmap('neutral.png')
        self.doubt=QPixmap('doubt.png')
        self.question=QPixmap('question_sizeup.png')
        self.question=self.question.scaledToWidth(200)

        self.lbl_img=QLabel()
        self.lbl_img.setPixmap(self.neutral)




        btn=QPushButton(self)
        btn.setIcon(QIcon('question.png'))
        btn.setCheckable(True)
        btn.clicked.connect(self.btn_clicked)

        vbox=QVBoxLayout()

        vbox.addWidget(self.lbl_img)
        vbox.addWidget(btn)


        self.setLayout(vbox)
        self.setWindowTitle('Untacticon UI')
        self.resize(200,300)
        self.center()
        self.show()

    def btn_clicked(self):
        #QMessageBox.about(self,"message","질문하였습니다.")
        self.lbl_img.setPixmap(self.question)
        time.sleep(1)
        #self.lbl_img.setPixmap(self.doubt)



    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MyApp()
    sys.exit(app.exec_())
