import cv2
import numpy as np

img = cv2.imread('IMG_4823.jpg')
x, y = img.shape[0:2]
img = cv2.resize(img, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
cv2.imshow('Origin', img)  # 显示图片
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
imgCopy = img.copy()


# 按照官网方法只能画出一条直线
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
    print("rho:{}, theta:{}".format(rho, theta))
    print("(x1,y1):{}".format((x1, y1)))
    print("(x2,y2):{}".format((x2, y2)))

# 正确做法是如此，以下三种方法都可
# # 方法一：在原来的三维数组中迭代
for line in lines:
    rho = line[0][0]  # 第一个元素是距离rho
    theta = line[0][1]  # 第二个元素是角度theta
    # # 方法二：在原来的三维数组中迭代
    # for i in range(0, lines.shape[0]):
    #     rho, theta = lines[i, 0]
    # # 方法三：先将三维数组转变为二维，再迭代
    # lines = lines[:, 0, :]  # 提取为为二维
    # print("new lines", lines)
    # for line in lines:
    #     rho = line[0]  # 第一个元素是距离rho
    #     theta = line[1]  # 第二个元素是角度theta
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(imgCopy, (x1, y1), (x2, y2), (0, 0, 255), 1)

cv2.imshow('Edged', edges)  # 显示图片
cv2.imshow('Hough_Old', img)  # 显示图片
cv2.imshow('Hough_New', imgCopy)  # 显示图片
cv2.waitKey(0)

