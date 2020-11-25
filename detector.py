from imutils.video import VideoStream
from imutils import face_utils
import imutils
import dlib
import cv2
import time
from queue import Queue
from scipy.spatial import distance as dist


class MyDetector:

    # sleep 관련
    STATE = "normal"
    COUNTER = 0
    TOTAL = 0

    EYE_AR_THRESH = 0.3
    SLEEP_CONSEC_FRAMES = 30

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def get_ear(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def detect_sleep(self, shape, frame, state, state_changed):
        leftEye = shape[self.lStart: self.lEnd]
        rightEye = shape[self.rStart:self.rEnd]
        leftEAR = self.get_ear(leftEye)
        rightEAR = self.get_ear(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)

        # 졸음 감지
        if ear < self.EYE_AR_THRESH:  # 눈을 감았을 때
            self.COUNTER += 1

            # 눈을 계속 감고 있는 경우 -> 졸음이라고 판단
            if self.COUNTER >= self.SLEEP_CONSEC_FRAMES:
                self.STATE = "sleep!"
                state = 3
                state_changed.emit('{}'.format(state))

        else:  # 눈을 떴을 때
            self.COUNTER = 0
            self.STATE = "normal"
            state = 1
            state_changed.emit('{}'.format(state))

        # 화면에 표시
        # cv2.putText(frame, "COUNTER: {}".format(self.COUNTER), (10, 30),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # cv2.putText(frame, "USER STATE: {}".format(self.STATE), (300, 30),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    def video(self, detect, detect_changed, state, state_changed):



        # 모델 불러오기
        print('load model...')
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("public/shape_predictor_68_face_landmarks.dat")

        # video stream 시작
        print('start video stream')
        vs = VideoStream(0).start()
        time.sleep(2.0)




        print('start detecting')
        while True:

            frame = vs.read()
            frame = imutils.resize(frame, width=600)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 0)

            detect = "0"

            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                self.detect_sleep(shape, frame, state, state_changed)

                detect = "1"

            detect_changed.emit('{}'.format(detect))


            cv2.imshow("webcam", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("1"):
                state = 1
                state_changed.emit('{}'.format(state))
            if key == ord("2"):
                sec = 2
                state_changed.emit('{}'.format(state))

            if key == ord("q"):
                break



## __main__

if __name__=='__main__':
    q = Queue()
    # t = threading.Thread(target=MyDetector.video(q), args=(q,))
    # t.start()
    md = MyDetector()
    md.video(q)

