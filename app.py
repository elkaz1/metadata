import os
import tempfile
import streamlit as st
from moviepy.editor import VideoFileClip

# Streamlit Web App
st.title("Video Metadata Removal Tool")
st.write("Upload videos, and this tool will remove their metadata.")

# File upload section
uploaded_files = st.file_uploader(
    "Upload your video files (multiple files are supported)", 
    type=["mp4", "mov", "avi", "mkv"], 
    accept_multiple_files=True
)

if uploaded_files:
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        cleaned_files = []

        # Process each uploaded file
        for uploaded_file in uploaded_files:
            input_file_path = os.path.join(temp_dir, uploaded_file.name)
            
            # Save uploaded file to the temp directory
            with open(input_file_path, "wb") as f:
                f.write(uploaded_file.read())

            # Output file path
            output_file_path = os.path.join(temp_dir, f"cleaned_{uploaded_file.name}")
            
            # Remove metadata by re-encoding video
            try:
                video = VideoFileClip(input_file_path)
                video.write_videofile(output_file_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
                cleaned_files.append(output_file_path)
            except Exception as e:
                st.error(f"An error occurred while processing {uploaded_file.name}: {e}")
        
        if cleaned_files:
            # Provide individual download links
            st.success(f"Metadata has been removed from {len(cleaned_files)} videos successfully!")
            for cleaned_file in cleaned_files:
                with open(cleaned_file, "rb") as f:
                    cleaned_video = f.read()
                st.download_button(
                    label=f"Download Cleaned Video: {os.path.basename(cleaned_file)}",
                    data=cleaned_video,
                    file_name=os.path.basename(cleaned_file),
                    mime="video/mp4"
                )
