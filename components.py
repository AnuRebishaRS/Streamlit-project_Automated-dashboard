import streamlit as st
import time

# Text & Headers

st.header("This is a header")
st.subheader("This is a subheader")
st.text("This is some regular text.")
st.markdown("This is **Markdown** text with *italic* and **bold** formatting.")


st.caption("This is a caption text.")
st.code("print('Hello, Streamlit!')", language='python')
st.json({"name": "Streamlit", "type": "library", "language": "Python"})
st.latex(r"E = mc^2")
st.write("This is a versatile write function that can display text, data, and more.")
st.title("This is a title")
st.success("This is a success message.")
st.info("This is an info message.")
st.warning("This is a warning message.")
st.error("This is an error message.")
st.exception("This is an exception message.")
st.metric("Temperature", "25 °C", "+1.5 °C")
st.balloons()
st.snow()
st.toast("This is a toast notification!", icon="🎉")
st.progress(0.5)

if st.button("Show Spinner"):
    with st.spinner("Please wait..."):
        time.sleep(2)
    st.success("Done!")

# Buttons

if st.button("Click Me"):
    st.error("Button clicked!")

# Sliders & Inputs

age = st.slider("Select Age", 1, 100, 25)
name = st.text_input("Enter your name:")

if st.button("Submit"):
    st.write(f"Hello, {name}! You are {age} years old.")

# File Uploader

import pandas as pd
from PIL import Image
from pathlib import Path

st.title("File Upload and Viewer")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["txt", "csv", "xlsx", "png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    st.write("**File name:**", uploaded_file.name)
    st.write("**File size:**", f"{uploaded_file.size:,} bytes")
    st.write("**File type:**", uploaded_file.type)

    # Get the file extension
    file_extension = Path(uploaded_file.name).suffix.lower()

    # Display image files
    if file_extension in [".png", ".jpg", ".jpeg"]:
        st.subheader("Uploaded Image")

        image = Image.open(uploaded_file)
        st.image(
            image,
            caption=uploaded_file.name,
            use_container_width=True
        )

    # Display tabular data files
    elif file_extension == ".csv":
        st.subheader("Uploaded DataFrame")
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

    elif file_extension == ".xlsx":
        st.subheader("Uploaded Excel Data")
        df = pd.read_excel(uploaded_file)
        st.dataframe(df, use_container_width=True)

    elif file_extension == ".txt":
        st.subheader("Uploaded Text File")
        text = uploaded_file.getvalue().decode("utf-8")
        st.text_area("File contents", text, height=300)