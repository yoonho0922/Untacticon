from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import dlib
import cv2
import threading
import time
from queue import Queue

def detector(q):
    # 모델 불러오기
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # video stream 시작
    vs = VideoStream(0).start()
    time.sleep(2.0)

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            for (x, y) in shape:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        cv2.imshow("webcam", frame)
        key = cv2.waitKey(1) & 0xFF



        if key == ord("1"):
            print(1)
            q.put("1번")
        if key == ord("2"):
            print(2)
            q.put("2번")

        if key == ord("q"):
            break

## __main__

if __name__=='__main__':
    q = Queue()

    t = threading.Thread(target=sum, args=(q,))
    t.start()

    i = 0
    while True:
        print("main thread {}".format(i))
        i = i + 1
        print(q.empty())
        if q.empty() == False:
            data = q.get()
            print(data)

        time.sleep(1)
