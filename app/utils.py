from typing import List
import cv2
import numpy as np

def images_to_video(image_files: List[str], output_path: str, fps: int = 10):
    images = [cv2.imread(img_fp) for img_fp in image_files]
    if not images or images[0] is None:
        # Handle case where no images are found or the first image can't be read
        raise ValueError("Could not read images or no images provided.")
    height, width, layers = images[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for img in images:
        if img is not None:
            video.write(img)
    video.release()
    return output_path 