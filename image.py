
import streamlit as st
import base64
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title="Image Gallery",
    layout="wide"
)

# ---------- Folder Paths ----------
BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "image"
BACKGROUND_PATH = IMAGE_DIR / "background.jpg"

# ---------- Transparent / Faded Background ----------
if BACKGROUND_PATH.exists():
    encoded = base64.b64encode(
        BACKGROUND_PATH.read_bytes()
    ).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(
                    rgba(255, 255, 255, 0.70),
                    rgba(255, 255, 255, 0.70)
                ),
                url("data:image/png;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- Page Title ----------
st.title("My Image Gallery")
st.write("Explore the collection of 10 images.")

st.divider()

# ---------- Image Details ----------
images = [
    ("Image 1", "image1.jpg"),
    ("Image 2", "image2.jpg"),
    ("Image 3", "image3.jpg"),
    ("Image 4", "image4.jpg"),
    ("Image 5", "image5.jpg"),
    ("Image 6", "image6.jpg"),
    ("Image 7", "image7.jpg"),
    ("Image 8", "image8.jpg"),
    ("Image 9", "image9.jpg"),
    ("Image 10", "image10.jpg"),
]

# ---------- Display Gallery ----------
for start in range(0, len(images), 3):
    cols = st.columns(3, gap="large")

    for col, (caption, filename) in zip(
        cols, images[start:start + 3]
    ):
        image_path = IMAGE_DIR / filename

        with col:
            if image_path.exists():
                st.image(
                    str(image_path),
                    caption=caption,
                    use_container_width=True
                )
            else:
                st.warning(f"Image not found: {filename}")

    st.write("")
