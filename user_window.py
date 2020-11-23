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
        self.neutral=QPixmap('public/neutral.png')
        self.question=QPixmap('public/question_sizeup.png')
        self.question=self.question.scaledToWidth(200)
        self.doubt = QPixmap('public/doubt.png')
        self.tired=QPixmap('public/tired.png')
        self.being_left=QPixmap('public/being left.png')
        self.yes=QPixmap('public/yes.png')
        self.no=QPixmap('public/no.png')



        self.lbl_img=QLabel()
        self.lbl_img.setPixmap(self.neutral)




        btn=QPushButton(self)
        self.btn2 = QPushButton()
        self.btn2.setText("back")
        self.bt2=0
        btn.setIcon(QIcon('public/question.png'))
        btn.clicked.connect(self.btn_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)


        self.vbox=QVBoxLayout()

        self.vbox.addWidget(self.lbl_img)
        self.vbox.addWidget(btn)




        self.setLayout(self.vbox)
        self.setWindowTitle('Untacticon UI')
        self.resize(200,300)
        self.center()
        self.show()




    def btn_clicked(self):
        #QMessageBox.about(self,"message","질문하였습니다.")
        self.lbl_img.setPixmap(self.question)
        self.bt2=self.vbox.addWidget(self.btn2)

    def btn2_clicked(self):
        self.lbl_img.setPixmap(self.neutral)
        self.vbox.itemAt(2).widget().setParent(None)

    def keyPressEvent(self, e):
        if e.key()==Qt.Key_1:
            self.lbl_img.setPixmap(self.neutral)
        elif e.key()==Qt.Key_2:
            self.lbl_img.setPixmap(self.doubt)
        elif e.key()==Qt.Key_3:
            self.lbl_img.setPixmap(self.tired)
        elif e.key()==Qt.Key_4:
            self.lbl_img.setPixmap(self.being_left)
        elif e.key()==Qt.Key_5:
            self.lbl_img.setPixmap(self.yes)
        elif e.key()==Qt.Key_6:
            self.lbl_img.setPixmap(self.no)








    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MyApp()
    sys.exit(app.exec_())
