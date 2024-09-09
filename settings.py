import sys
import os

FILE = os.path.dirname(os.path.abspath(__file__))
ROOT = FILE

if ROOT not in sys.path:
    sys.path.append(ROOT)
    
image = 'Image'
video = 'Video'
webcam = 'Webcam'
youtube = 'YouTube'
sources = [image, video, webcam, youtube]

img_dir = os.path.join(ROOT, 'Images')

video_dir = os.path.join(ROOT, 'Videos')

model_dir = os.path.join(ROOT, 'weight')
detection_model = os.path.join(model_dir, 'yolov8n.pt')
segmentation_model = os.path.join(model_dir, 'yolov8n-seg.pt')

webcam_path = 0