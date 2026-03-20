import streamlit as st
import cv2
import numpy as np
import tempfile
from moviepy.editor import VideoFileClip
from engine import process_frame

st.title("Hallaf AI Real Estate PRO 🔥")

uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov"])

if uploaded_file:
    st.info("Processing... ⏳")

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    clip = VideoFileClip(tfile.name)

    def process(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = process_frame(frame)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    new_clip = clip.fl_image(process)

    output = "output.mp4"
    new_clip.write_videofile(output, codec="libx264")

    st.success("Done 🔥")

    video = open(output, "rb")
    st.video(video.read())

    st.download_button("Download Video", video, file_name="hallaf_pro.mp4") 
