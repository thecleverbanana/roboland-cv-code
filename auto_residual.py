import cv2
import numpy as np
import os

# 指定视频路径和输出文件夹
video_path = "path/to/your/video.avi"
output_folder = "path/to/output/frames/"
os.makedirs(output_folder, exist_ok=True)

# 输入时间点（秒数）
start_time = 10  # 从 10 秒开始处理，修改为你的需要

# 打开视频文件
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 设置起始时间
fps = int(cap.get(cv2.CAP_PROP_FPS))  # 获取帧率
cap.set(cv2.CAP_PROP_POS_FRAMES, start_time * fps)

# 读取第一帧作为初始关键帧
ret, frame_a = cap.read()
if not ret:
    print(f"Error: Could not read the initial frame at {start_time} seconds.")
    cap.release()
    exit()

current_time = start_time  # 当前时间（秒）
frame_count = 0  # 用于保存帧的编号

while True:
    # 跳过 3 秒钟的帧
    current_time += 3
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_time * fps)
    ret, frame_b = cap.read()

    if not ret:
        print("End of video reached or error reading frame.")
        break

    # 计算残差图像
    residual_image = cv2.absdiff(frame_a, frame_b)

    # 保存残差图像
    output_path = os.path.join(output_folder, f"residual_frame_{frame_count:04d}.jpg")
    cv2.imwrite(output_path, residual_image)
    print(f"Saved residual image: {output_path}")

    # 更新关键帧 A
    frame_a = frame_b.copy()
    frame_count += 1

# 释放视频捕获对象
cap.release()
print("Processing complete.")
