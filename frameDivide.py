import os
import cv2
import xml.etree.ElementTree as ET

# Paths
xmlPath = "data/originData/video/2-2/2-2_cam01_assault01_place04_night_spring.xml"
videoPath = "data/originData/video/2-2/2-2_cam01_assault01_place04_night_spring.mp4"
outputImagePath = (
    "data/inputData/image/2-2_cam01_assault01_place04_night_spring_punching"
)

# Parse XML
tree = ET.parse(xmlPath)
root = tree.getroot()

# Find frames with actionname "punching"
punchingFrames = set()
for action in root.findall(".//action[actionname='punching']/frame"):
    startFrame = int(action.find("start").text)
    endFrame = int(action.find("end").text)
    punchingFrames.update(range(startFrame, endFrame + 1))

# Open video
cap = cv2.VideoCapture(videoPath)
frameWidth = int(cap.get(3))
frameHeight = int(cap.get(4))
fps = int(cap.get(5))

# Define codec and output video
# 윈도우면
# fourcc = cv2.VideoWriterFourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(outputImagePath, fourcc, fps, (frameWidth, frameHeight))

frameCount = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frameCount += 1

    # If frame is in punching_frames, write to output video
    if frameCount in punchingFrames:
        out.write(frame)

    # Stop when all punching frames are processed
    if frameCount > max(punchingFrames):
        break

cap.release()
out.release()

print("Output video with punching frames created at:", outputImagePath)
