import cv2
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
from utils.stamp import add_stamp

import streamlit as st
def stamp_pdf(pdf_paths, stamp_img, poppler_path, output_names, size=(250,250)):

    for pdf_path, output_name in zip(pdf_paths, output_names):
        pdf_pages = convert_from_path(pdf_path, poppler_path=poppler_path)
        stamp_img = cv2.resize(stamp_img, size)

        stamped_pages = []
        for idx, page in enumerate(pdf_pages):
            page = np.array(page)
            stamped_page = add_stamp(page, stamp_img, False, False)
            stamped_page = Image.fromarray(stamped_page.astype('uint8'), 'RGB')
            stamped_pages.append(stamped_page)
        
        stamped_pages[0].save(
            output_name, "PDF", resolution=100.0, save_all=True, append_images=stamped_pages[1:]
        )

    st.success(f"{len(pdf_paths)} Files Stamped Succesfully in the `stamped_pdfs` directory")
    # print(f"File Saved Successfully with {output_name} name.")