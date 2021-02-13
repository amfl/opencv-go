import cv2
import numpy as np

def generate_board_mask(frame_hsv):
    """Isolates the rough shape of the board by color matching.
    Returns the biggest group of connected pixels that is roughly the color of the board.
    This mask probably doesn't need to be generated every frame."""
    lower = (8, 0, 0)  # H,S,V
    upper = (64, 255, 255)
    mask = cv2.inRange(frame_hsv, lower, upper)

    # Erode/Dilate to remove noise
    kernel_3 = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask, kernel_3, iterations = 1)
    dilation = cv2.dilate(erosion, kernel_3, iterations = 3)
    return dilation

def find_board_contour(frame_gray_blur):
    # Detect edges using Canny
    threshold = 250
    canny_output = cv2.Canny(frame_gray_blur, threshold, threshold * 3)

    # Find contours
    contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find longest contours
    # drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    # for i in range(len(contours)):
    #     color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    #     cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)

    contour_longest = max(contours, key=lambda x: cv2.arcLength(x, True))
    contour_approx = cv2.approxPolyDP(contour_longest, cv2.arcLength(contour_longest, True) * 0.03, True)

    # Find the convex hull object for each contour
    contour_hull = cv2.convexHull(contour_approx)

    return contour_hull

