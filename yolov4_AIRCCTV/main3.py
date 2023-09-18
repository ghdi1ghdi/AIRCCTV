import cv2
import numpy as np

CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGTH = 480

capture = cv2.VideoCapture(CAMERA_ID)
if capture.isOpened() == False:
    print(f"Can't open the Camera({CAMERA_ID})")
    exit()

capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGTH)

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
VideoSignal.set(3, 720)
VideoSignal.set(4, 1080)
fourcc = cv2.VideoWriter_fourcc(*"avci")

# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet(
    "/Users/jack/Documents/GitHub/AIRCCTV/yolov4_AIRCCTV/yolov4-tiny-custom.cfg",
    "/Users/jack/Documents/GitHub/AIRCCTV/yolov4_AIRCCTV/yolov4-tiny-custom_best.weights",
)

classes = []
with open(
    "/Users/jack/Documents/GitHub/AIRCCTV/yolov4_AIRCCTV/ClassNames.names", "r"
) as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

video_writer = None  # <-- 이름을 변경했습니다

while True:
    ret, frame = VideoSignal.read()
    h, w, c = frame.shape

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
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)

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

            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
            cv2.putText(frame, label, (x, y + 30), font, 3, color, 2)

            if class_ids[i] in [0, 2]:
                if video_writer is None:  # <-- 변경된 이름을 사용
                    video_writer = cv2.VideoWriter("save.mp4", fourcc, 25.0, (640, 480))
                video_writer.write(frame)

    cv2.imshow("YOLOv4", frame)
    if cv2.waitKey(1) > 0:
        break

if video_writer is not None:
    video_writer.release()

VideoSignal.release()
cv2.destroyAllWindows()
