import cv2
import numpy as np
import glob
import os

# 指定包含视频文件的文件夹路径
video_folder = "original_video/11-13"
output_folder = "frame_difference_output/11-13"

# 检查输出文件夹是否存在，不存在则创建
os.makedirs(output_folder, exist_ok=True)

# 遍历文件夹中的所有 .avi 文件
for video_path in glob.glob(os.path.join(video_folder, "*.avi")):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    print(f"Processing video: {video_name}")

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 读取第一帧
    ret, frame1 = cap.read()
    if not ret:
        print(f"Error: Could not read the first frame of {video_name}.")
        cap.release()
        continue

    # 跳到视频的最后一帧
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1)
    ret, frame2 = cap.read()
    if not ret:
        print(f"Error: Could not read the last frame of {video_name}.")
        cap.release()
        continue

    # 计算帧差
    frame_diff = cv2.absdiff(frame1, frame2)

    # 保存结果
    output_path = os.path.join(output_folder, f"{video_name}_frame_diff.jpg")
    cv2.imwrite(output_path, frame_diff)
    print(f"Frame difference image saved as {output_path}")

    # 释放视频捕获对象
    cap.release()

print("Processing complete for all videos.")
