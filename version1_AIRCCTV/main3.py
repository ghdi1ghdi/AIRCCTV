from cProfile import label
import cv2
import numpy as np
import pygame as sd

# import winsound as sd (윈도우)
import time

CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGTH = 480

capture = cv2.VideoCapture(CAMERA_ID)
if capture.isOpened() == False:  # 카메라 정상상태 확인
    print(f"Can't open the Camera({CAMERA_ID})")
    exit()

capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGTH)


def beepsound():
    fr = 2000
    du = 2000
    sd.Beep(fr, du)


# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
VideoSignal.set(3, 720)
VideoSignal.set(4, 1080)
fc = 20.0
codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")
count = 99
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov4-tiny-custom.cfg", "yolov4-tiny-custom_best.weights")

# YOLO NETWORK 재구성
classes = []
with open("ClassNames.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    h, w, c = frame.shape

    # YOLO 입력
    blob = cv2.dnn.blobFromImage(
        frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False
    )
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_point = (
                    detection[1] - detection[0],
                    detection[2] - detection[0],
                )
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # 사각형
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 1)

    font = cv2.FONT_ITALIC
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(frame, label, (x, y + 30), font, 3, (255, 0, 0), 2)
            # 경계상자와 클래스 정보 이미지에 입력
            if class_ids[i] == 0:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, label, (x, y + 30), font, 3, (0, 255, 0), 2)
                print(
                    "width :%d, height : %d" % (VideoSignal.get(3), VideoSignal.get(4))
                )
                fourcc = cv2.VideoWriter_fourcc(*"DIVX")
                out = cv2.VideoWriter("save.avi", fourcc, 25.0, (640, 480))
                while True:
                    ret, frame = VideoSignal.read()  # Read 결과와 frame
                    if ret:
                        gray = cv2.cvtColor(
                            frame, cv2.COLOR_BGR2GRAY
                        )  # 입력 받은 화면 Gray로 변환
                        # cv2.imshow('frame_color', frame)    # 컬러 화면 출력        cv2.imshow('frame_gray', gray)    # Gray 화면 출력
                        out.write(frame)
                        if cv2.waitKey(1) == ord("q"):
                            break
                        cv2.destroyAllWindows()
            elif class_ids[i] == 2:
                beepsound()
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 3)
                cv2.putText(frame, label, (x, y + 30), font, 3, (255, 0, 255), 2)
                print(
                    "width :%d, height : %d" % (VideoSignal.get(3), VideoSignal.get(4))
                )
                fourcc = cv2.VideoWriter_fourcc(*"DIVX")
                out = cv2.VideoWriter("save.avi", fourcc, 25.0, (640, 480))
                while True:
                    ret, frame = VideoSignal.read()  # Read 결과와 frame
                    if ret:
                        gray = cv2.cvtColor(
                            frame, cv2.COLOR_BGR2GRAY
                        )  # 입력 받은 화면 Gray로 변환
                        # cv2.imshow('frame_color', frame)    # 컬러 화면 출력        cv2.imshow('frame_gray', gray)    # Gray 화면 출력
                        out.write(frame)
                        if cv2.waitKey(1) == ord("q"):
                            break
                        cv2.destroyAllWindows()
    cv2.imshow("YOLOv4", frame)
    if cv2.waitKey(1) > 0:
        break
