import cv2
import numpy as np
import torch
from pathlib import Path
import time

CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

capture = cv2.VideoCapture(CAMERA_ID)
if capture.isOpened() == False:
    print(f"Can't open the Camera({CAMERA_ID})")
    exit()

capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# Load YOLOv5 model
model_path = Path("/Users/jack/Documents/GitHub/AIRCCTV/last.pt")
model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    "/Users/jack/Documents/GitHub/AIRCCTV/last.pt",
)
model.eval()

# Class names
with open(
    "/Users/jack/Documents/GitHub/AIRCCTV/yolov4_AIRCCTV/ClassNames.names", "r"
) as f:
    classes = [line.strip() for line in f.readlines()]

video_writer = None
recording = False
start_time = None
end_time = None

while True:
    ret, frame = capture.read()
    if not ret:
        break

    # Inference
    results = model(frame)
    pred = results.pred[0]

    for *xyxy, conf, cls in pred:
        x1, y1, x2, y2 = map(int, xyxy)
        label = f"{classes[int(cls)]} {conf:.2f}"

        if int(cls) == 0:  # 클래스가 "public" (예: 0)일 때만 모자이크 처리
            roi = frame[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(roi, (99, 99), 0)  # 모자이크 처리
            frame[y1:y2, x1:x2] = blurred_roi
        else:
            # 다른 클래스 레이블에 따라 색상 지정
            if int(cls) == 1:  # "attacker" 클래스 (예: 1)
                color = (0, 0, 255)  # 빨간색
            elif int(cls) == 2:  # "victim" 클래스 (예: 2)
                color = (255, 0, 0)  # 파란색

            # 박스 그리기
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                3,
            )
            cv2.putText(
                frame,
                label,
                (x1, y1),
                cv2.FONT_ITALIC,
                0.6,
                color,
                2,
            )

            # attacker 감지 시 녹화 시작
            if int(cls) == 1 and not recording:
                recording = True
                start_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
                video_writer = cv2.VideoWriter(
                    f"recording_{start_time}.mp4",
                    cv2.VideoWriter_fourcc(*"mp4v"),
                    25.0,
                    (FRAME_WIDTH, FRAME_HEIGHT),
                )

    # 녹화 중이면 프레임을 녹화 파일에 추가
    if recording:
        video_writer.write(frame)

        # 녹화 시작 시간으로부터 3초가 경과하면 녹화 종료
        if (
            time.time() - time.mktime(time.strptime(start_time, "%Y-%m-%d-%H:%M:%S"))
            >= 3
        ):
            recording = False
            end_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
            video_writer.release()
            print(f"Recording ended. Start time: {start_time}, End time: {end_time}")

    cv2.imshow("YOLOv5", frame)
    if cv2.waitKey(1) > 0:
        break

if video_writer is not None:
    video_writer.release()

capture.release()
cv2.destroyAllWindows()
