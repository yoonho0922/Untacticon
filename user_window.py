from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import cv2
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import dlib
import cv2
import threading
import time
from PyQt5.QtGui import QPixmap
import detector

class MyMainGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.btn1 = QPushButton("Start", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl_img)
        vbox.addWidget(self.btn1)
        self.setLayout(vbox)

        self.setGeometry(100, 50, 300, 300)

class Test:
    def __init__(self):
        name = ""


class MyMain(MyMainGUI):
    add_sec_signal = pyqtSignal()
    send_instance_singal = pyqtSignal("PyQt_PyObject")

    def __init__(self, parent=None):
        super().__init__(parent)

        self.btn1.clicked.connect(self.start)

        self.th = Worker(parent=self)
        self.th.sec_changed.connect(self.state_update)  # custom signal from worker thread to main thread

        self.show()

    @pyqtSlot()
    def start(self):
        self.th.start()
        self.th.working = True

    @pyqtSlot(str)
    def state_update(self, msg):
        if msg == "1":
            self.lbl_img.setPixmap(self.neutral)
        elif msg == "2":
            self.lbl_img.setPixmap(self.doubt)
        elif msg == "3":
            self.lbl_img.setPixmap(self.tired)
        elif msg == "4":
            self.lbl_img.setPixmap(self.being_left)
        elif msg == "5":
            self.lbl_img.setPixmap(self.yes)
        elif msg == "6":
            self.lbl_img.setPixmap(self.no)



class Worker(QThread):
    sec_changed = pyqtSignal(str)

    def __init__(self, state=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True
        self.state = state

        # self.main.add_sec_signal.connect(self.add_sec)   # 이것도 작동함. # custom signal from main thread to worker thread

    def __del__(self):
        print(".... end thread.....")
        self.wait()

    def run(self):

        md = detector.MyDetector()
        md.video(self.state, self.sec_changed)
        # print('load model...')
        # detector = dlib.get_frontal_face_detector()
        # # predictor = dlib.shape_predictor("public/shape_predictor_68_face_landmarks.dat")
        #
        # print('start video stream')
        # vs = VideoStream(0).start()
        # time.sleep(2.0)
        #
        # print('start detecting')
        # while self.working:
        #         frame = vs.read()
        #         frame = imutils.resize(frame, width=400)
        #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #
        #         rects = detector(gray, 0)
        #
        #         # for rect in rects:
        #             # shape = predictor(gray, rect)
        #             # shape = face_utils.shape_to_np(shape)
        #             #
        #             # for (x, y) in shape:
        #             #     cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        #
        #         cv2.imshow("webcam", frame)
        #         key = cv2.waitKey(1) & 0xFF
        #
        #         if key == ord("1"):
        #             self.sec = 1
        #             self.sec_changed.emit('{}'.format(self.sec))
        #         if key == ord("2"):
        #             self.sec = 2
        #             self.sec_changed.emit('{}'.format(self.sec))
        #         if key == ord("3"):
        #             self.sec = 3
        #             self.sec_changed.emit('{}'.format(self.sec))
        #         if key == ord("4"):
        #             self.sec = 4
        #             self.sec_changed.emit('{}'.format(self.sec))
        #         if key == ord("5"):
        #             self.sec = 5
        #             self.sec_changed.emit('{}'.format(self.sec))
        #         if key == ord("6"):
        #             self.sec = 6
        #             self.sec_changed.emit('{}'.format(self.sec))
        #
        #         if key == ord("q"):
        #             break



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()