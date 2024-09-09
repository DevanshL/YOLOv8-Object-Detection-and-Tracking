import cv2 as cv
import streamlit as st
import settings
from ultralytics import YOLO
import yt_dlp


def load_model(model_path):
    model = YOLO(model_path)
    return model


def display_tracker_options():
    tracker = st.radio("Display Tracker", ('Yes', 'No'))
    if tracker == 'Yes':
        is_display_tracker = True
    else:
        is_display_tracker = False
        
    if is_display_tracker:
        tracker_type = st.radio("Tracker Type", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None


def display_detect_frame(conf, model, st_frame, img, is_display_track=None, tracker=None):
    img = cv.resize(img, (720, int(720 * (9/16))))
    
    if is_display_track:
        res = model.track(img, conf=conf, persist=True, tracker=tracker)
    else:
        res = model.predict(img, conf=conf)
        
    # frame on detected objects
    plot = res[0].plot()
    st_frame.image(plot, caption='Detected Video', channels='BGR', use_column_width=True)
    

def ytube_stream_url(url):
    ydl_ops = {
        'format': 'best[ext=mp4]',
        'no_warnings': True,
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']
    
    
def play_ytube_video(conf, model):
    ytube_url = st.sidebar.text_input("Enter YouTube URL")
    is_display_track, tracker_type = display_tracker_options()
    
    if st.sidebar.button('Detect Object'):
        if not ytube_url:
            st.warning("Please Enter YouTube URL")
            return
        
        try:
            st.sidebar.info("Please wait, loading video...")
            stream_url = ytube_stream_url(ytube_url)
            
            st.sidebar.info("Video loaded successfully")
            cap = cv.VideoCapture(stream_url)
            
            if not cap.isOpened():
                st.error("Error loading video")
                return
            
            st.sidebar.info("Video is playing...")
            st_frame = st.empty()
            while cap.isOpened():
                success, img = cap.read()
                if success:
                    display_detect_frame(conf, model, st_frame, img, is_display_track, tracker_type)
                else:
                    break
            
            cap.release()
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
            
def webcam_stream(conf, model):
    data = settings.webcam_path if settings.webcam_path else 0
    is_display_track, tracker_type = display_tracker_options()
    if st.sidebar.button('Detect Object'):
        cap = None
        try:
            cap = cv.VideoCapture(data)
            st_frame = st.empty()

            if not cap.isOpened():
                st.error("Error accessing webcam")
                return

            while cap.isOpened():
                success, img = cap.read()
                if success:
                    display_detect_frame(conf, model, st_frame, img, is_display_track, tracker_type)
                else:
                    break

        except Exception as e:
            st.error(f"Error: {str(e)}")

        finally:
            if cap is not None:
                cap.release()


def play_stored_video(conf, model):
    video = st.sidebar.selectbox("Select Video", settings.video_dict.keys())
    is_display_track, tracker_type = display_tracker_options()
    
    with open(settings.video_dict[video], 'rb') as vid:
        video_bytes = vid.read()
        if video_bytes:
            st.video(video_bytes)
        
    if st.sidebar.button('Detect Object'):
        try:
            cap = cv.VideoCapture(str(settings.video_dict.get(video)))
            st_frame = st.empty()
            
            if not cap.isOpened():
                st.error("Error loading video")
                return
            
            while cap.isOpened():
                success, img = cap.read()
                if success:
                    display_detect_frame(conf, model, st_frame, img, is_display_track, tracker_type)
                else:
                    cap.release()
                    break
                
        except Exception as e:
            cap.release()
            st.error(f"Error: {str(e)}")
