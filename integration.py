# USAGE
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2

import numpy as np

class MyDetector:
    # 전역 변수

    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('./hello.avi', fourcc, 20.0, (1024, 768))  # 창 크기 조절

    # define movement threshodls
    max_head_movement = 20
    movement_threshold = 50
    gesture_threshold = 100

    gesture = False
    x_movement = 0
    y_movement = 0
    gesture_show = 20  # number of frames a gesture is shown

    stop_cnt = 0
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 전역 변수로 설정해서 for문에서 빼오기
    x_center = 0
    y_center = 0
    p0 = 0
    p1 = 0

    x_up = 0
    y_up = 0
    x_down = 0
    y_down = 0

    a_cot = 0
    b_cot = 0

    gradient_a = 1
    gradient_b = 1

    keep_cnt = 0

    def get_coords(self, p1):
        try:
            return int(p1[0][0][0]), int(p1[0][0][1])
        except:
            return int(p1[0][0]), int(p1[0][1])

    def maximum(self, n1, n2):
        if (n1 > n2):
            return n1
        else:
            return n2


    def video(self):
        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print("[INFO] loading facial landmark predictor...")
        detector = dlib.get_frontal_face_detector()  # 얼굴 영역 검출하는 부분
        predictor = dlib.shape_predictor(
            "public/shape_predictor_68_face_landmarks.dat")  # predictor 모델 가져오기 # 얼굴 안에서 눈코입 찾는 부분

        ## 어디서 오래걸리는건지도 확인

        # initialize the video stream and allow the cammera sensor to warmup
        print("[INFO] camera sensor warming up...")
        # cap = cv2.VideoCapture(0)
        time.sleep(2.0)

        while True:
            ## 얼굴 인식
            ret, old_frame = cap.read()
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)  # from color to black and white
            rects = detector(old_gray, 0)  # x,y
            ret, frame = cap.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 얘는 밖으로 빼도 되겠다

            ## 특정 부위 좌표 찾기
            for rect in rects:
                shape = predictor(frame_gray, rect)
                shape = face_utils.shape_to_np(shape)
                x_center, y_center = shape[30]  # 34는 너무 콧구멍
                x_up, y_up = shape[28]
                x_down, y_down = shape[8]

            ## 찾은 좌표 사용하여 광학 흐름 측정하기
            face_up = x_up, y_up
            p0_up = np.array([[face_up]], np.float32)
            face_center = x_center, y_center  # 특정 부위 좌표 저장
            p0_center = np.array([[face_center]], np.float32)  # Numpy array로 형변환
            face_down = x_down, y_down
            p0_down = np.array([[face_down]], np.float32)

            p1_up, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0_up, None,
                                                      **lk_params)  # 광학 흐름 함수 사용하여 점 추적
            p1_center, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0_center, None,
                                                          **lk_params)  # 광학 흐름 함수 사용하여 점 추적
            p1_down, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0_down, None,
                                                        **lk_params)  # 광학 흐름 함수 사용하여 점 추적

            cv2.circle(frame, get_coords(p0_up), 3, (0, 255, 0))
            cv2.circle(frame, get_coords(p1_up), 3, (255, 0, 0), -1)  # 파란색이 따라다니는 점
            cv2.circle(frame, get_coords(p0_center), 3, (0, 0, 255))  # 빨간색이 나한테 붙어있는 점
            cv2.circle(frame, get_coords(p1_center), 3, (255, 0, 0), -1)  # 파란색이 따라다니는 점
            cv2.circle(frame, get_coords(p0_down), 3, (0, 255, 0))
            cv2.circle(frame, get_coords(p1_down), 3, (255, 0, 0), -1)  # 파란색이 따라다니는 점

            ## 정수로 좌표화
            a_up, b_up = get_coords(p0_up), get_coords(p1_up)
            a_down, b_down = get_coords(p0_down), get_coords(p1_down)

            a, b = get_coords(p0_center), get_coords(p1_center)
            print("p0_center is ", p0_center)
            print("p1_center is ", p1_center)
            print("a is ", a)
            print("b is ", b)

            ## 움직임 최소화하기
            if abs(a[0] - b[0]) > 5 or abs(
                    a[1] - b[1]) > 5 and x_movement > 0 and y_movement > 0:  # 이것에 대한 임계값은 해보면서 계속 찾아보기
                x_movement += abs(a[0] - b[0])
                y_movement += abs(a[1] - b[1])
                gradient_a += (x_movement / y_movement) + 1
                gradient_b += (y_movement / x_movement) + 1

            print("x_movement is ", x_movement)
            print("y_movement is ", y_movement)
            print("gesture_show is ", gesture_show)

            ## movement 글씨로 표시
            text = 'x_movement: ' + str(x_movement)
            if not gesture: cv2.putText(frame, text, (50, 50), font, 0.8, (0, 0, 255), 2)  # x_movement 글씨 표시
            text = 'y_movement: ' + str(y_movement)
            if not gesture: cv2.putText(frame, text, (50, 100), font, 0.8, (0, 0, 255), 2)  # y_movement 글씨 표시

            if x_movement > gesture_threshold or y_movement > gesture_threshold:
                if x_movement > gesture_threshold and keep_cnt <= 0:
                    print(">>> Gesture is No, x_movement is ", x_movement)
                    gesture = 'No'
                    keep_cnt = 20

                if y_movement > gesture_threshold and keep_cnt <= 0:
                    print(">>> Gesture is Yes, y movement is ", y_movement)
                    gesture = 'Yes'
                    keep_cnt = 20

                print("abs(a_cot - b_cot) is ", abs(a_cot - b_cot))

            else:
                if abs(a_up[0] - a_down[0]) >= 1 and abs(b_up[0] - b_down[0]) >= 1:
                    a_cot = abs(a_up[0] - a_down[0]) / abs(a_up[1] - a_down[1]) * 100
                    b_cot = abs(b_up[0] - b_down[0]) / abs(b_up[1] - b_down[1]) * 100
                    print("cot is ", a_cot)
                    print("cot is ", b_cot)

                    print(" >>>> Two cot size is ", abs(a_cot - b_cot))
                    print("abs(a_cot - b_cot) is ", abs(a_cot - b_cot))
                    print("maximum(gradient_a/gradient_b, gradient_b/gradient_a) is ",
                          maximum(gradient_a / gradient_b, gradient_b / gradient_a))

                    if abs(a_cot - b_cot) > 10 and abs(a_cot - b_cot) < 20 and maximum(gradient_a / gradient_b,
                                                                                       gradient_b / gradient_a) < 8 and keep_cnt <= 0:  # 얘가 아무때나 안 나오도록 제한 조건을 걸어주는 것도 나쁘지 않음
                        print(">>> Gesture is Doubt")
                        gesture = 'Doubt'
                        keep_cnt = 10

            text = 'gradient_a: ' + str(gradient_a)
            if not gesture: cv2.putText(frame, text, (50, 150), font, 0.8, (255, 0, 0), 2)
            text = 'gradient_b: ' + str(gradient_b)
            if not gesture: cv2.putText(frame, text, (50, 200), font, 0.8, (255, 0, 0), 2)
            text = 'Doubt: ' + str(abs(a_cot - b_cot))
            if not gesture: cv2.putText(frame, text, (50, 250), font, 0.8, (255, 0, 0), 2)
            ## gesture 임계값을 넘기면 긍정 및 부정 인식식
            # 도리도리는 150 / 끄덕끄덕은 30 정도 움직임
            # 원래는 gesture_threshold 값을 가짐
            # 반응이 아니어도 움직임이 허용되는 선의 범위 안에서 gesture_threshold를 정해야 함

            # 의문 상황은 대각선으로 움직이는 것을 포착하면 되는데
            # 이 상황이 위에 상황과 겹쳐지면 어떻게 해야 하나를 지금 생각 중
            # 좀 더 강력하게 구분될 수 있는 상황을 만들어야겠음
            # 각 증분에 대한 기울기

            ## 긍정 혹은 부정 표현이 감지되었을 때 이를 얼마나 유지할 것인가
            if gesture and gesture_show > 0:
                cv2.putText(frame, 'Gesture Detected: ' + gesture, (50, 50), font, 1.2, (0, 0, 255), 3)
                gesture_show -= 1  # 1씩 감소

            ## 0까지 갔을 때는 다시 특정 임계값으로 올린 다음에 다시 시작
            if gesture_show == 0:
                gesture = False
                x_movement = 1
                y_movement = 1  # 움직임이 없으면 0으로 초기화시키네
                gradient_a = 1
                gradient_b = 1
                gesture_show = 20  # number of frames a gesture is shown

            ##### 고개가 자연스럽게 움직일 수 있는 부분에서 허용되는 범위 #####
            # 자연스럽게 고개가 움직이는 부분은 어떻게 할 것이냐
            # 근데 이 count가 Gesture를 파악하는데 걸림돌이 되면 안된다
            if stop_cnt > 30:  # 30 정도면 되는 것이냐
                x_movement = 1
                y_movement = 1
                gradient_a = 1
                gradient_b = 1
                stop_cnt = 0

            stop_cnt += 1
            keep_cnt = keep_cnt - 1

            out.write(frame)
            cv2.waitKey(1)

            ## 화면에 보여주고 종료 커맨드
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            # Deallocation
        cv2.destroyAllWindows()


    # Deallocation
    cv2.destroyAllWindows()

if __name__=='__main__':

    md = MyDetector()
    md.video()