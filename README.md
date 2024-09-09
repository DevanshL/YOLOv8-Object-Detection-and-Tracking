# YOLOv8-Object-Detection-and-Tracking
This project is a real-time object detection and tracking application using YOLOv8 pre-trained model built with This repository showcases an extensive open-source project that integrates real-time object detection and tracking using YOLOv8, a state-of-the-art object detection algorithm, with Streamlit, a powerful Python web application framework. This project provides an intuitive and customizable interface that allows users to detect and track objects in real-time video streams from various sources such as  UDP, YouTube URLs, as well as static videos and images.


## HomePage
![homepage](https://github.com/DevanshL/YOLOv8-Object-Detection-and-Tracking/blob/main/assests/home.png)


## Image Detection and Tracking

Detected Image         |  Segemented Image
:-------------------------:|:-------------------------:
![detected_image](https://github.com/DevanshL/YOLOv8-Object-Detection-and-Tracking/blob/main/Images/detected_image3.jpg)  |  ![Segemnted_image](https://github.com/DevanshL/YOLOv8-Object-Detection-and-Tracking/blob/main/Images/segmented_image3.jpg)



## Tracking With Object Detection with help of Ytube url

https://github.com/user-attachments/assets/630cb165-f21b-4fce-90e6-495f48c7276d

##  Object Detection and Tracking by Video uploading

https://github.com/user-attachments/assets/97683897-e538-4520-a820-783bf1a2e102


https://github.com/user-attachments/assets/e959a8f8-b377-402c-bb13-b71f974896b6



## Requirements

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/DevanshL/YOLOv8-Object-Detection-and-Tracking.git
```

2. Change to the repository directory:

```bash
cd yolov8-streamlit-detection-tracking
```

3. Create directories for weights, videos, and images:

```bash
mkdir weights videos images
```

4. Download the pre-trained YOLOv8 weights:

Save the downloaded `weights` to the weights directory.

```bash
https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

## Usage

1. Run the app:

```bash
streamlit run app.py
```

2. Interact with the app:

The app should open in a new browser window.


## ML Model Config

* `Select task`: Choose between detection or segmentation.
* `Set model confidence`: Use the slider to adjust the confidence threshold (25-100%).

## Object Detection on Images

* `Default image`: The default image with detected objects is displayed.
* `Upload an image`: Click the "Browse files" button to upload your image.
* `Run detection`: Click the "Detect Objects" button to run detection with the chosen confidence threshold.
* `Download the result`: If "Save Detected (or) Segmented Image to Download" is selected, click "Download Image" to save the output.

## Object Detection in Videos

* `Prepare videos`: Place your video files in the videos folder.
* `Update settings`: Edit settings.py to match your video file names.
* `Run detection`: Choose a video in the app and click "Detect Video Objects."

## Object Detection on YouTube Video URL

* `Select source`: Choose "YouTube."
* `Enter URL`: Paste the YouTube video URL in the textbox.
* `Run detection`: The detection/segmentation task will start automatically

## Acknowledgements
This app leverages YOLOv8 for object detection and the Streamlit library for the user interface.


