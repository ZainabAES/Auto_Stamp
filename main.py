import streamlit as st
import os
import cv2
import numpy as np

import config
from utils.general import new_line, get_hw_ratio
from utils.pdf import stamp_pdf
from utils.stamp import color_adjustment

st.header("Auto Stamp")
st.subheader(" Stamp Documents with a Single Click! ")
st.divider()

st.subheader("Enter PDF Folder Path")
folder_path = st.text_input("Enter Folder Path", placeholder="Enter the Path that contains the PDF Files...")

st.subheader("Upload your Stamp")
stamp = st.file_uploader("Upload your stamp!", type=["jpg", "png", "jpeg"])

if folder_path and stamp:
    files = os.listdir(folder_path)
    pdf_files = [os.path.join(folder_path, file) for file in files if file.endswith(".pdf")]
    stamp = cv2.imdecode(np.frombuffer(stamp.read(), np.uint8), 1)
    stamp = color_adjustment(stamp)
    hw_ratio = get_hw_ratio(stamp)

    new_line()
    st.divider()
    new_line()

    # Folder creation......
    stamped_dir_name = "stamped_pdfs"
    stamped_dir_name = os.path.join(folder_path, stamped_dir_name)
    os.makedirs(stamped_dir_name, exist_ok=True)

    with st.expander("Tune Parameters"):
        # Background Parameters ... STOP

        # Stamp Size
        st.subheader("Stamp Size")
        st.write("Select the Required Stamp Size....")
        user_width = st.slider("Stamp Width Size", min_value=50, max_value=1000, value=stamp.shape[1], step=10, help="Set the Required Stamp Width Size...")
        user_height = user_width * hw_ratio
        stamp_size = (int(user_width), int(user_height))
        st.image(stamp, width=user_width)

    output_names = [os.path.join(stamped_dir_name, os.path.basename(pdf_file)) for pdf_file in pdf_files]
    if st.button("Stamp", on_click=stamp_pdf, args=(pdf_files, stamp, config.poppler_path, output_names, stamp_size), key="stamp_button"):
        st.success(f"{len(pdf_files)} Files Stamped Succesfully in the `stamped_pdfs` directory")

