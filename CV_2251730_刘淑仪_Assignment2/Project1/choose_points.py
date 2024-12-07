import cv2

# 全局变量，用于存储点击的点
points = []


# 鼠标点击事件回调函数
def click_event(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        # 将点击的坐标保存到 points 列表
        points.append([x, y])
        # 在点击位置画一个小圆圈
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        # 显示点击的坐标
        cv2.putText(img, f'({x},{y})', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        # 显示更新后的图像
        cv2.imshow("Image", img)

        print(f"点击的点: ({x}, {y})")  # 打印点击的坐标

        # 如果已经点击了4个点，输出坐标并退出
        if len(points) == 4:
            print("\n选取的四个点：")
            for i, p in enumerate(points, 1):
                print(f"点 {i}: {p}")
            cv2.waitKey(0)  # 等待按键退出


# 加载图像
img = cv2.imread('img_src/src_7.jpg')  # 替换为你图像的路径
cv2.imshow("Image", img)

# 设置鼠标回调函数
cv2.setMouseCallback("Image", click_event)

# 持续等待鼠标事件
cv2.waitKey(0)
cv2.destroyAllWindows()