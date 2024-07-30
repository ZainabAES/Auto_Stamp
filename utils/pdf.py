"""
PDF Utilites for Auto Sampoing Project
"""
import cv2
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
from utils.stamp import add_stamp

def stamp_pdf(pdf_paths, stamp_img, poppler_path, output_names, size=(409, 214)):
    """
    Stamp PDF
    """
    for pdf_path, output_name in zip(pdf_paths, output_names):
        pdf_pages = convert_from_path(pdf_path, poppler_path=poppler_path)
        stamp_img = cv2.resize(stamp_img, size)
        stamped_pages = []
        for page in pdf_pages:
            page = np.array(page)
            stamped_page = add_stamp(page, stamp_img, False, False)
            stamped_page = Image.fromarray(stamped_page.astype('uint8'), 'RGB')
            stamped_pages.append(stamped_page)
        stamped_pages[0].save(
            output_name, "PDF", resolution=100.0, save_all=True, append_images=stamped_pages[1:]
        )
