"""
General Utilities for Auto Stampint Project.
"""
import streamlit as st
from pdf2image import convert_from_path, convert_from_bytes
import config
import numpy as np
from PIL import Image
from utils.stamp import add_stamp
def new_line(n=1):
    """
    Adding New Line into Streamlit UI.

    Parameters:
    -----------
    n: int
        number of reuired added new lines.
    """
    for _ in range(n):
        st.write("\n")

def get_hw_ratio(img):
    """
    Calculate Height Widht Ratio

    Parameters:
    ----------
    img: np.ndarray
        stamp img

    Return:
    ------
    hw_ratio: float
        ratio between height and width
    """
    h, w = img.shape[:2]
    hw_ratio = h / w
    return hw_ratio

def get_max_width_size(pdf_paths,poppler_path):
    """
    This function is resbonsible for geting the maximum width of the documnets 
    """
    pages_width= []
    for pdf_path in pdf_paths:
        # st.write(f"PDF PATH: {pdf_path}")
        # pdf_pages = convert_from_path(pdf_path,poppler_path=poppler_path)
        pdf_pages = convert_from_bytes(pdf_path, poppler_path=poppler_path)
        for page in pdf_pages:
            page = np.array(page)
            h,w=page.shape[:2]
            pages_width.append(w)
    return min(pages_width)




