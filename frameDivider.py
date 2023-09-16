import cv2

count = 1
test = 1
train = 1

for i in range(1, 5):
    # 비디오 경로
    vidcap = cv2.VideoCapture("/Users/jack/Desktop/영상/%d.mp4" % i)

    print("%d번째 영상 시작" % i)

    while vidcap.isOpened():
        ret, image = vidcap.read()

        if ret == False:
            print("%d번째 영상 끝" % i)
            print("train=%d" % train)
            print("test=%d" % test)
            break

        if int(vidcap.get(1)) % 30 == 0:  # 1프레임씩 저장
            num = count % 10

            if num == 0 or num == 5:  # 20%는 test data, 80%는 train data
                cv2.imwrite(
                    "/Users/jack/Documents/GitHub/AIRCCTV/data/inputData/image/test/%s.jpg"
                    % str(test).zfill(5),
                    image,
                )
                test += 1
            else:
                cv2.imwrite(
                    "/Users/jack/Documents/GitHub/AIRCCTV/data/inputData/image/train/%s.jpg"
                    % str(train).zfill(5),
                    image,
                )
                train += 1

            count += 1

    vidcap.release()

print("devide end")
vidcap.release()
