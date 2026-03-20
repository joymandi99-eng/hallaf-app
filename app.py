from engine import process_frame
import streamlit as st
import cv2
import numpy as np
import tempfile
from moviepy.editor import VideoFileClip

st.title("Hallaf AI Real Estate Effect 🎬")

uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov"])


    
    # تحويل للصورة الرمادية
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # كشف الحواف
    edges = cv2.Canny(gray, 100, 200)
    
    # تحويل الحواف إلى لون أخضر (ستايل الحلاف)
    green_edges = np.zeros_like(frame)
    green_edges[:,:,1] = edges
    
    # دمج الصورة الأصلية مع التأثير
    output = cv2.addWeighted(frame, 0.7, green_edges, 0.8, 0)
    
    # تعتيم الخلفية (تقريبي)
    mask = cv2.GaussianBlur(edges, (21,21), 0)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
    
    final = frame * mask + output * (1 - mask)
    return final.astype(np.uint8)

if uploaded_file:
    st.info("Processing video... ⏳")

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    clip = VideoFileClip(tfile.name)
    
  def process(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = process_frame(frame)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    new_clip = clip.fl_image(process_frame)

    output_path = "output.mp4"
    new_clip.write_videofile(output_path, codec="libx264")

    st.success("Done! 🎉")

    video_file = open(output_path, "rb")
    st.video(video_file.read())

    st.download_button("Download Video", video_file, file_name="hallaf_output.mp4")
