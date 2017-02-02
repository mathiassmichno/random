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
font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 255, 0)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

print("Found {} faces".format(len(faces)))
show_image = np.copy(image)
for i, (x, y, w, h) in enumerate(faces):
    cv2.rectangle(show_image, (x,y), (x+w,y+h), color, 2)
    cv2.putText(show_image, "Face {}".format(i), (x,y+h), font, 1, (255,255,0), 2)

cv2.imshow("Faces", show_image)
cv2.waitKey(0)
choice = input("Select faces (seperate by comma):")
choice = [int(x.strip()) for x in choice.split(',') if x.strip().isdigit()]

for j in choice::
    x, y, w, h = faces[j]
    folder_path = path.join("./", path.splitext(path.basename(img_path))[0], str(j))
    print(folder_path)
    makedirs(folder_path)
    tmp = np.copy(image)
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
