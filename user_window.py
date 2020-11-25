from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import detector
from PyQt5.QtGui import QIcon

class MyMainGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.detect_on=QPixmap('public/detect_on.png').scaledToWidth(10)
        self.detect_off=QPixmap('public/detect_off.png')

        self.neutral=QPixmap('public/neutral.png')
        self.question=QPixmap('public/question_sizeup.png')
        self.doubt = QPixmap('public/doubt.png')
        self.tired=QPixmap('public/tired.png')
        self.being_left=QPixmap('public/being left.png')
        self.yes=QPixmap('public/yes.png')
        self.no=QPixmap('public/no.png')

        # 얼굴인식 여부
        self.detectDot = QLabel()
        self.detectDot.resize(10,10)
        self.detectDot.setPixmap(self.detect_off)
        self.detectText = QLabel('인식안됨', self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.detectDot)
        hbox.addWidget(self.detectText)

        # 사용자 이모티콘
        self.userEmoticon = QLabel()
        self.userEmoticon.setPixmap(self.neutral)

        # 질문 버튼
        self.questionBtn = QPushButton(self)
        self.questionBtn.setIcon(QIcon('public/question.png'))

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.userEmoticon)
        vbox.addWidget(self.questionBtn)
        self.setLayout(vbox)
        self.setGeometry(100, 50, 200, 300)

class Test:
    def __init__(self):
        name = ""


class MyMain(MyMainGUI):
    add_sec_signal = pyqtSignal()
    send_instance_singal = pyqtSignal("PyQt_PyObject")

    def __init__(self, parent=None):
        super().__init__(parent)

        # video 스레드
        self.th = Worker(parent=self)
        self.th.detect_changed.connect(self.detect_update)  # custom signal from worker thread to main thread
        self.th.state_changed.connect(self.state_update)  # custom signal from worker thread to main thread
        self.th.start()
        self.th.working = True
        
        self.show()

    @pyqtSlot(str)
    def detect_update(self, msg):
        # 검출 안됨
        if msg == "0":
            self.detectDot.setPixmap(self.detect_off)
            self.detectText.setText("인식 안됨")
        elif msg == "1":
            self.detectDot.setPixmap(self.detect_on)
            self.detectText.setText("인식 중")

    @pyqtSlot(str)
    def state_update(self, msg):
        if msg == "1":
            self.userEmoticon.setPixmap(self.neutral)
        elif msg == "2":
            self.userEmoticon.setPixmap(self.doubt)
        elif msg == "3":
            self.userEmoticon.setPixmap(self.tired)
        elif msg == "4":
            self.userEmoticon.setPixmap(self.being_left)
        elif msg == "5":
            self.userEmoticon.setPixmap(self.yes)
        elif msg == "6":
            self.userEmoticon.setPixmap(self.no)



class Worker(QThread):
    detect_changed = pyqtSignal(str)
    state_changed = pyqtSignal(str)

    def __init__(self, detect = 0,state=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True
        self.detect = detect
        self.state = state

        # self.main.add_sec_signal.connect(self.add_sec)   # 이것도 작동함. # custom signal from main thread to worker thread

    def __del__(self):
        print(".... end thread.....")
        self.wait()

    def run(self):

        md = detector.MyDetector()
        md.video(self.detect, self.detect_changed, self.state, self.state_changed)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()