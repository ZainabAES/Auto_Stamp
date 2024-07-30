"""
General Utilities for Auto Stampint Project.
"""
import streamlit as st

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
