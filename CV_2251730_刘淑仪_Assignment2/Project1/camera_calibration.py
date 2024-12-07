import cv2
import numpy as np

# 读取标定板图片
images = []
for i in range(1, 11):
    img = cv2.imread(f"img_src/src_{i}.jpg")
    images.append(img)

# 定义棋盘格的角点数
rows = 6
cols = 9

# 定义棋盘格的边长
size = 0.02  # 单位为米

# 定义标定板的世界坐标
obj_points = np.zeros((rows * cols, 3), np.float32)
obj_points[:, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 2) * size

# 定义存储特征点的列表
img_points = []  # 棋盘格角点的图像坐标
obj_points_list = []  # 对应的世界坐标

# 遍历每张图片，检测特征点
for img in images:
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 检测棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, (rows, cols), None)
    # 如果检测到，添加到列表中
    if ret:
        img_points.append(corners)
        obj_points_list.append(obj_points.copy())

# 标定相机，获取内参矩阵和畸变系数
# 使用最后一张图像的灰度图像尺寸作为标定的输入尺寸
gray = cv2.cvtColor(images[0], cv2.COLOR_BGR2GRAY)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points_list, img_points, gray.shape[::-1], None, None)

print("ret: ")
print(ret)
print("mtx: ")
print(mtx)
print("dist: ")
print(dist)
print("rvecs: ")
print(rvecs)
print("tvecs: ")
print(tvecs)

# 读取待处理的图像（注意这里是读取需要去畸变的图像）
original_img = cv2.imread('img_src/src_7.jpg')

# 去畸变
img_undistort = cv2.undistort(original_img, mtx, dist, None, mtx)  # 使用标定得到的内参和畸变系数

# 定义源点和目标点
src_points = np.float32([
    [136, 28],  # 左上角
    [1008, 68],  # 右上角
    [1117, 628],  # 右下角
    [165, 806]   # 左下角
])
dst_points = np.float32([
    [0, 0],  # 左上角
    [1440, 0],  # 右上角
    [1440, 810],  # 右下角
    [0, 810]   # 左下角
])

# 计算透视变换矩阵
M = cv2.getPerspectiveTransform(src_points, dst_points)

# 透视变换
img_warp = cv2.warpPerspective(img_undistort, M, (1920, 810))

# 显示图像
cv2.imshow("Original", original_img)
cv2.imshow("Undistort", img_undistort)
cv2.imshow("Warp", img_warp)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存结果
cv2.imwrite("result/Original.jpg", original_img)
cv2.imwrite("result/Undistorted.jpg", img_undistort)
cv2.imwrite("result/Bird View.jpg", img_warp)
