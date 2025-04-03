import streamlit as st
import os
from PIL import Image

# Directory for images
image_dir = 'images'  # Ensure this directory exists and contains images

def display_image_gallery():
    """Display a day-wise image gallery."""
    st.title("Day-wise Image Gallery")
    
    days = os.listdir(image_dir)
    for day in days:
        st.subheader(f"Day {day}")
        images = os.listdir(os.path.join(image_dir, day))
        for image in images:
            img_path = os.path.join(image_dir, day, image)
            img = Image.open(img_path)
            st.image(img, caption=image, use_column_width=True)

if __name__ == "__main__":
    display_image_gallery()
