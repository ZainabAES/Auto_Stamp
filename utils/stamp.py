"""
Module Docstring
"""
from typing import Union
import cv2
import numpy as np
from PIL import Image

def get_roi(doc, stamp):
    """
    Function Docstring
    """
    h, w, _ = doc.shape

    starting_h = h - stamp.shape[0]
    ending_h = h

    middle_w  = w // 2
    starting_w = middle_w - stamp.shape[1]//2
    ending_w = starting_w + stamp.shape[1]

    roi = doc[starting_h: ending_h, starting_w:ending_w, :]
    return roi, starting_h, ending_h, starting_w, ending_w


def get_whitespace_ratio(window):
    """
    Function Docstring
    """
    counter = 0
    img = Image.fromarray(window.astype('uint8'), 'RGB')
    img = img.convert("RGBA")
    pixels = img.getdata()
    for pixel in pixels:
        # print(f"PIXEL: {pixel}")
        if pixel == (255, 255, 255, 255):
            counter += 1
    return counter

def get_max_idx(counter_dict):
    """
    Function Docstring
    """
    lst = [window["counter"] for window in counter_dict.values()]
    idx = lst.index(max(lst))
    return idx

def whitespace_area(doc, stamp):
    """
    Function Docstring
    """
    stamp_h, stamp_w = stamp.shape[:2]
    doc_h, doc_w = doc.shape[:2]

    white_ratio_dict: dict[int, dict[str, Union[tuple, int]]] = {}
    for starting_heigh in range(0, doc_h, stamp_h):
        for starting_width in range(0, doc_w, stamp_w):
            ending_width = starting_width + stamp_w
            ending_heigh = starting_heigh + stamp_h
            roi = doc[starting_heigh: ending_heigh, starting_width:ending_width, :]

            dict_index = len(white_ratio_dict) #?
            white_ratio_dict[dict_index] = {
                "coord": (starting_heigh, ending_heigh, starting_width, ending_width),
                "counter": get_whitespace_ratio(roi)
            }
    max_idx = get_max_idx(white_ratio_dict)
    coord = white_ratio_dict[max_idx]["coord"]
    starting_heigh, ending_heigh, starting_width, ending_width = coord
    roi = doc[starting_heigh: ending_heigh, starting_width:ending_width, :]

    return roi, starting_heigh, ending_heigh, starting_width, ending_width


def add_stamp(doc, stamp, resize_show_ratio=0.75, imshow = False, imwrite = False):
    """
    Function Docstring
    """
    #stamp = color_adjustment(stamp)
    stamp = Image.fromarray(stamp.astype('uint8'), 'RGB')
    stamp = background_removal(stamp)
    stamp = stamp.convert('RGB')
    stamp = np.array(stamp)

    _, starting_h, ending_h, starting_w, ending_w = whitespace_area(doc, stamp)
    doc[starting_h: ending_h, starting_w:ending_w, :] = stamp
    if imshow:
        show_doc = doc.copy()
        show_doc = cv2.resize(show_doc, None, fx=resize_show_ratio, fy=resize_show_ratio)
        cv2.imshow("DOC", show_doc)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if imwrite:
        pass

    return doc

from PIL import Image
import numpy as np

def add_stamp_Pillow(doc, stamp, resize_show_ratio=0.75, imshow=False, imwrite=False):
    """
    Function Docstring
    """
    # Convert numpy array to PIL Image
    stamp = Image.fromarray(stamp.astype('uint8'), 'RGB')
    
    # Perform background removal and color adjustment if necessary
    stamp = background_removal(stamp)
    stamp = stamp.convert('RGB')
    
    # Convert back to numpy array for manipulation
    stamp = np.array(stamp)
    
    # Find the whitespace area and place the stamp
    _, starting_h, ending_h, starting_w, ending_w = whitespace_area(doc, stamp)
    doc[starting_h:ending_h, starting_w:ending_w, :] = stamp
    
    if imshow:
        # Convert the document to PIL Image
        show_doc = Image.fromarray(doc.astype('uint8'), 'RGB')
        
        # Resize the document for display
        width, height = show_doc.size
        show_doc = show_doc.resize((int(width * resize_show_ratio), int(height * resize_show_ratio)), Image.ANTIALIAS)
        
        # Show the document
        show_doc.show()
    
    if imwrite:
        # Save the document if needed (not implemented)
        pass
    
    return doc

def color_adjustment(image):
    """
    Function Docstring
    """
    stamp_img=image
    if stamp_img.shape[2] == 4:
        stamp_img = cv2.cvtColor(stamp_img, cv2.COLOR_RGBA2BGR)
    else:
        stamp_img = cv2.cvtColor(stamp_img, cv2.COLOR_RGB2BGR)
    return stamp_img

from PIL import Image

def color_adjustment_pillow(image):
    """
    Adjusts the color of the image if needed.
    """
    stamp_img = Image.fromarray(image)

    if stamp_img.mode == 'RGBA':
        stamp_img = stamp_img.convert('RGB')
    
    return np.array(stamp_img)

def background_removal(stamp):
    """
    Function Docstring
    """
    stamp = stamp.convert("RGBA")
    pixels = stamp.getdata()
    new_data = []

    for item in pixels:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    stamp.putdata(new_data)
    stamp.save("./New.png", "PNG")
    return stamp
