import cv2
import numpy as np
from typing import Union
from PIL import Image

def get_roi(doc, stamp):
    h, w, _ = doc.shape

    starting_h = h - stamp.shape[0]
    ending_h = h

    middle_w  = w // 2
    starting_w = middle_w - stamp.shape[1]//2
    ending_w = starting_w + stamp.shape[1]

    roi = doc[starting_h: ending_h, starting_w:ending_w, :]
    return roi, starting_h, ending_h, starting_w, ending_w 


def get_whitespace_ratio(window):
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
    lst = [window["counter"] for window in counter_dict.values()]
    idx = lst.index(max(lst))
    return idx
    
def whitespace_area(doc, stamp):
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
    print(f"ALL DICT: {white_ratio_dict}")
    max_idx = get_max_idx(white_ratio_dict)
    print(f"MAX IDX: {max_idx}")
    coord = white_ratio_dict[max_idx]["coord"]
    starting_heigh, ending_heigh, starting_width, ending_width = coord
    roi = doc[starting_heigh: ending_heigh, starting_width:ending_width, :]

    return roi, starting_heigh, ending_heigh, starting_width, ending_width


def add_stamp(doc, stamp, resize_show_ratio=0.75, imshow = False, imwrite = False):
    #stamp = color_adjustment(stamp)
    stamp = Image.fromarray(stamp.astype('uint8'), 'RGB')
    stamp = background_removal(stamp)
    stamp = stamp.convert('RGB') #i think this should be removed felt its unnecessry
    stamp = np.array(stamp)
    # stamp = cv2.imread(stamp)
    # cv2.imshow(f"STAMP", stamp)
    # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()

    roi, starting_h, ending_h, starting_w, ending_w = whitespace_area(doc, stamp)
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

def color_adjustment(image):
    stamp_img=image
    if stamp_img.shape[2] == 4:
        stamp_img = cv2.cvtColor(stamp_img, cv2.COLOR_RGBA2BGR)
    else:
        stamp_img = cv2.cvtColor(stamp_img, cv2.COLOR_RGB2BGR)
    return stamp_img

def background_removal(stamp):
    stamp = stamp.convert("RGBA")
    pixels = stamp.getdata()
    newData = []
 
    for item in pixels:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    stamp.putdata(newData)
    stamp.save("./New.png", "PNG")
    return stamp
