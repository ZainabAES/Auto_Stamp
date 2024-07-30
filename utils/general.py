import streamlit as st

def new_line(n=1):
    for _ in range(n):
        st.write("\n")

def get_hw_ratio(img):
    h, w = img.shape[:2]
    hw_ratio = h / w
    return hw_ratio