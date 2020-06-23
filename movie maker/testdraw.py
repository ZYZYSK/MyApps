import numpy as np
import cv2
img = np.zeros((512, 512, 3), np.uint8)
# cv2.line(img,開始座標,終了座標,RGB,太さ)
img = cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)
img = cv2.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)
# cv2.circle(img,中心,半径,色,太さ<-1で内側塗りつぶし>)
img = cv2.circle(img, (447, 63), 63, (0, 0, 255), -1)
# cv2.ellipse(img,中心、長径と短径,偏角,始角,終角,太さ<-1で内側塗りつぶし>)
img = cv2.ellipse(img, (256, 256), (100, 50), 0, 0, 180, 255, -1)
# 多角形 http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html
pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
pts = pts.reshape((-1, 1, 2))
img = cv2.polylines(img, [pts], True, (0, 255, 255))
# 文字
font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(img,文字列、開始座標、フォントの種類、大きさ、色、太さ、線の種類)
cv2.putText(img, 'OpenCV4.0', (10, 500), font,
            3, (255, 255, 255), 1, cv2.LINE_AA)


cv2.imwrite('draw.png', img)
