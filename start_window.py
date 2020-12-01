import sys
import user_window
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import*
from PyQt5 import uic

start_window=uic.loadUiType('public/example01.ui')[0]



class MyApp(QMainWindow,start_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn1.clicked.connect(lambda:self.btn_clicked())
        self.btn1.clicked.connect(lambda:self.close())




    def btn_clicked(self):
        newUi=user_window.MyMain()


if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=MyApp()
    ex.show()
    sys.exit(app.exec_())
