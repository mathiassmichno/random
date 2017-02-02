import cv2
import sys
import numpy as np
from random import randint
from os import makedirs, path

img_path = sys.argv[1]
casc_path = "/usr/local/opt/opencv3/share/openCV/haarcascades/haarcascade_frontalface_default.xml"
num = 100

face_cascade = cv2.CascadeClassifier(casc_path)
image = cv2.imread(img_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

print("Found {} faces".format(len(faces)))
show_image = np.copy(image)
for j, (x, y, w, h) in enumerate(faces):
    folder_path = path.join("./", path.splitext(path.basename(img_path))[0], str(j))
    print(folder_path)
    makedirs(folder_path)
    tmp = np.copy(image)
    color = (0, 255, 0)
    cv2.rectangle(show_image, (x,y), (x+w,y+h), color, 2)
    top_x = np.linspace(0, x, num)
    top_y = np.linspace(0, y, num)
    bot_x = np.linspace(image.shape[1], x+w, num)
    bot_y = np.linspace(image.shape[0], y+h, num)
    for i in range(num):
        path_0 = path.join(folder_path, "{}0{}.png".format(str(j), str(i).zfill(len(str(num-1)))))
        cv2.imwrite(
                path_0,
                image[int(top_y[i]):int(bot_y[i]), int(top_x[i]):int(bot_x[i])])

        path_1 = path.join(folder_path, "{}1{}.png".format(str(j), str(num-1-i).zfill(len(str(num-1)))))
        cv2.imwrite(
                path_1,
                image[int(top_y[i]):int(bot_y[i]), int(top_x[i]):int(bot_x[i])])

cv2.imshow("Faces", show_image)
cv2.waitKey(0)
