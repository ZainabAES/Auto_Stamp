import cv2

def get_roi(doc, stamp):
    """
    """
    h, w, _ = doc.shape

    starting_h = h - stamp.shape[0]
    ending_h = h

    middle_w  = w // 2
    starting_w = middle_w - stamp.shape[1]//2
    ending_w = starting_w + stamp.shape[1]

    roi = doc[starting_h: ending_h, starting_w:ending_w, :]
    return roi, starting_h, ending_h, starting_w, ending_w


def add_stamp(doc, stamp, resize_show_ratio=0.75, imshow = False, imwrite = False):
    dst = bgremove(stamp)
    roi, starting_h, ending_h, starting_w, ending_w = get_roi(doc, stamp)
    doc[starting_h: ending_h, starting_w:ending_w, :] = dst
    if imshow:
        show_doc = doc.copy()
        show_doc = cv2.resize(show_doc, None, fx=resize_show_ratio, fy=resize_show_ratio)
        cv2.imshow("DOC", show_doc)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if imwrite:
        pass

    return doc

def bgremove(image, min_thresh=127, max_thresh=255):
    """
    Background Removal
    """
    myimage_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, baseline = cv2.threshold(myimage_grey,min_thresh,max_thresh,cv2.THRESH_TRUNC)
    _, background = cv2.threshold(baseline,min_thresh,max_thresh,cv2.THRESH_BINARY)
    _, foreground = cv2.threshold(baseline,min_thresh,max_thresh,cv2.THRESH_BINARY_INV)

    foreground = cv2.bitwise_and(image,image, mask=foreground)
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)

    finalimage = background+foreground
    return finalimage
