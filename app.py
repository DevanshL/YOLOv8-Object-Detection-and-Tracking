import streamlit as st
import settings
import helper
from pathlib import Path
from PIL import Image
import tempfile
import cv2
import os

st.set_page_config(
    page_title="Object Detection with YOLOv8",
    page_icon=":dove_of_peace:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Object Segmentation and Tracking with YOLOv8')
st.sidebar.header('ML Model Configuration')

model_type = st.sidebar.selectbox('Select Model', ['Detection', 'Segmentation'])
conf = float(st.sidebar.slider('Model Confidence', 25, 100, 40)) / 100

try:
    path = Path(settings.detection_model if model_type == 'Detection' else settings.segmentation_model)
    model = helper.load_model(path)
except Exception as e:
    st.error(f"Unable to load model: {path}")
    st.error(e)

st.sidebar.header('Image/Video Configuration')
file_type = st.sidebar.radio('Select File Type', settings.sources)

def save_detected_image(image, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    image.save(save_path)
    return st.success(f"Image saved to {save_path}")

def save_segmented_image(image, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    image.save(save_path)
    return st.success(f"Segmented Image saved to {save_path}")

def save_detected_video(video_file, save_path, model, conf):
    cap = cv2.VideoCapture(video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform detection
        res = model.predict(frame_rgb, conf=conf)
        plot = res[0].plot()[:, :, ::-1]  # Convert back to BGR for saving

        # Write the frame to the output video file
        out.write(plot)
    
    cap.release()
    out.release()
    return st.success(f"Video saved to {save_path}")

def save_segmented_video(video_file, save_path, model, conf):
    cap = cv2.VideoCapture(video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform segmentation
        res = model.predict(frame_rgb, conf=conf)
        plot = res[0].plot()[:, :, ::-1]  # Convert back to BGR for saving

        # Write the frame to the output video file
        out.write(plot)
    
    cap.release()
    out.release()
    return st.success(f"Segmented Video saved to {save_path}")

if 'plot' not in st.session_state:
    st.session_state.plot = None
if 'image_name' not in st.session_state:
    st.session_state.image_name = None
if 'video_processed' not in st.session_state:
    st.session_state.video_processed = False
if 'is_segmented' not in st.session_state:
    st.session_state.is_segmented = False

if file_type == settings.image:
    img_file = st.sidebar.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png', 'webp', 'bmp'])

    if img_file:
        st.session_state.image_name = os.path.splitext(img_file.name)[0]
        uploaded_img = Image.open(img_file)
        st.image(uploaded_img, caption='Uploaded Image', use_column_width=True)

        if st.sidebar.button('Detect Objects'):
            res = model.predict(uploaded_img, conf=conf)
            st.session_state.plot = res[0].plot()[:, :, ::-1]  # Convert BGR to RGB
            st.image(st.session_state.plot, caption='Detected Image', use_column_width=True)

            with st.expander('Results'):
                for s in res[0].boxes:
                    st.write(s)

        if model_type == 'Detection':
            save_button_label = 'Save Detected Image'
            save_function = save_detected_image
        else:
            save_button_label = 'Save Segmented Image'
            save_function = save_segmented_image

        if st.sidebar.button(save_button_label):
            if st.session_state.plot is None:
                st.warning("No image detected. Please detect objects first.")
            else:
                try:
                    detected_image_name = f"{'detected' if model_type == 'Detection' else 'segmented'}_{st.session_state.image_name}.jpg"
                    save_path = os.path.join(settings.img_dir, detected_image_name)
                    save_image = Image.fromarray(st.session_state.plot)
                    save_function(save_image, save_path)
                except Exception as e:
                    st.error(f"Error saving image: {e}")

    else:
        st.warning("Please upload an Image for detection.")

elif file_type == settings.video:
    video_file = st.sidebar.file_uploader("Upload Video", type=['mp4', 'avi', 'mov'])

    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())

        if st.sidebar.button('Detect Video'):
            cap = cv2.VideoCapture(tfile.name)
            stframe = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                res = model.predict(frame_rgb, conf=conf)
                plot = res[0].plot()

                stframe.image(plot, channels="RGB", use_column_width=True)

            st.session_state.video_processed = True
            cap.release()

        if model_type == 'Detection':
            save_button_label = 'Save Detected Video'
            save_function = save_detected_video
        else:
            save_button_label = 'Save Segmented Video'
            save_function = save_segmented_video

        if st.sidebar.button(save_button_label):
            if not st.session_state.video_processed:
                st.warning("No video detected. Please detect objects first.")
            else:
                try:
                    detected_video_name = f"{'detected' if model_type == 'Detection' else 'segmented'}_{os.path.splitext(video_file.name)[0]}.mp4"
                    save_path = os.path.join(settings.video_dir, detected_video_name)
                    save_function(tfile.name, save_path, model, conf)
                except Exception as e:
                    st.error(f"Error saving video: {e}")

        os.remove(tfile.name)

    else:
        st.warning("Please upload a video for detection.")

elif file_type == settings.webcam:
    helper.webcam_stream(conf, model)

elif file_type == settings.youtube:
    helper.play_ytube_video(conf, model)

else:
    st.error('Please select a valid source')
