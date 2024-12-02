import os
import tempfile
import streamlit as st
from moviepy import VideoFileClip

# Streamlit Web App
st.title("Video Metadata Removal Tool By Zack")

# File Upload
uploaded_files = st.file_uploader(
    "Upload your video files (multiple files are supported)", 
    type=["mp4", "mkv", "avi", "mov"], 
    accept_multiple_files=True
)

if uploaded_files:
    # Process each uploaded file
    for uploaded_file in uploaded_files:
        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
                temp_input.write(uploaded_file.read())
                input_path = temp_input.name

            # Process the video with MoviePy to remove metadata
            video = VideoFileClip(input_path)
            output_path = os.path.join(tempfile.gettempdir(), f"cleaned_{uploaded_file.name}")
            video.write_videofile(output_path, codec="libx264", audio_codec="aac")

            # Provide the cleaned file for download
            with open(output_path, "rb") as cleaned_file:
                st.download_button(
                    label=f"Download Cleaned File: {uploaded_file.name}",
                    data=cleaned_file,
                    file_name=f"cleaned_{uploaded_file.name}",
                    mime="video/mp4"
                )

            # Close the video clip
            video.close()

        except Exception as e:
            st.error(f"An error occurred while processing {uploaded_file.name}: {str(e)}")
