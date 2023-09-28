# AIRCCTV

![image](https://github.com/ghdi1ghdi/AIRCCTV/assets/73730434/8e9af11b-a109-4505-ae51-ba29ccacb2ce)

Arificial Intelligence Recording CCTV Project by ghdi1ghdi

## Award

- 📋 2022 9th Korea SW Convergence Hackathon Contest / finalist (Sejong region representative)
- 🎖️ 2022 National crisis-related digital-based crisis response contest / selected as an excellent example
- 🥇 2023 Public Safety Invention Challenge National Police Agency Task / Grand Prize Award Commissioner of the Korean Intellectual Property Office (1st place)

## Demonstration video

https://drive.google.com/file/d/1dYbCkjbKnYOXBOHc5cxuIPA7tp6DxeMh/view?usp=sharing

## Model detected image

![image](https://github.com/ghdi1ghdi/AIRCCTV/assets/73730434/6db6aa97-03fc-48d7-a7fc-63fb65c7d28f)

## What Is AIRCCTV

version 1. AIRCCTV is an abbreviation of AI Recording CCTV, and if artificial intelligence automatically judges a dangerous situation, a notification sounds, recording starts from that point, and the recording ends when the action ends and Ordinary people do mosaic processing.

version 2. your Personal AI CCTV in android and ios, AIRCCTV is an abbreviation of AI Recording CCTV, and if artificial intelligence automatically judges a dangerous situation, a notification sounds, recording starts from that point, and the recording ends when the action ends.

## How to use it

0. download pytorch, yolov5

   - pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
   - git clone https://github.com/ultralytics/yolov5 # clone
   - cd yolov5
   - pip install -r requirements.txt # install

1. add your path

   - main.py
   - edit model local path, classname local path

2. test my custom model

   - python detect.py --weights last.pt --conf 0.5 --source 0

3. use main.py

   - python -u "/localpath/AIRCCTV/main.py
   - python -u "/Users/jack/Documents/GitHub/AIRCCTV/main.py"

## Develop Environment

1. server

   - IDE : Visual Studio Code
   - Node.js
   - MySQL

2. web

   - IDE : Visual Studio Code
   - React.js
   - TypeScript

3. mobile

   - IDE : Android Studio
   - Dart
   - Flutter

4. AI
   - IDE : Visual Studio Code, Colab
   - Python
   - OpenCV
   - YOLO v5
   - labelimg
   - 이상행동 CCTV 영상 DATA (https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=171)

## Code Style

1. indentation

   - use tab for indentation.

2. variable and Function Names
   - camelCase
   - use lowercase letters for variable and function names.
   ```
   useIDName()
   ```
3. constants
   - Write constants in uppercase letters.
   - If necessary, use underscores to separate words.
   - Constants represent values that won't be modified.
   ```
   CONSTANTS
   ```
4. factor
   - String using " "
   ```
   "Hello World!"
   ```
   - char using ' '
   ```
   'a'
   ```
5. comments
   - Write comments in English and keep them concise and clear.
   ```
   //Hi! I'm comments!
   ```

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc
