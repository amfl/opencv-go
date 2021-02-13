import cv2
import sys
import numpy as np

video_source = sys.argv[1]
try:
    video_source = int(video_source)
except:
    # Ignore error - We're likely being passed a filename.
    pass
video_cap = cv2.VideoCapture(video_source)

frame_width = int(round(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
frame_height = int(round(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(frame_width, frame_height)

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
    contour_approx = cv2.approxPolyDP(contour_longest, cv2.arcLength(contour_longest, True) * 0.02, True)

    # Find the convex hull object for each contour
    contour_hull = cv2.convexHull(contour_approx)

    return contour_hull

frame_num = 0
board_mask = None
while True:
    ret, frame = video_cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if frame_num % 10 == 0:  # TODO: Do this per time rather than frames

        # Detect the board (Mask method)
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        board_mask = generate_board_mask(frame_HSV)

        # Detect the board (contour method)
        frame_mask_blur = cv2.blur(board_mask, (3,3))
        board_contour = find_board_contour(frame_mask_blur)

    corners = cv2.goodFeaturesToTrack(frame_gray,
            maxCorners=(19*19)+20,
            qualityLevel=0.01,
            minDistance=10,
            mask=board_mask)

    # Draw onto the image

    for corner in corners:
        x,y= corner[0]
        x= int(x)
        y= int(y)
        cv2.rectangle(frame, (x-10,y-10),(x+10,y+10),(255,0,0),-1)

    cv2.drawContours(frame, [board_contour], -1, (255,255,255), 2)

    cv2.imshow("goodFeaturesToTrack Corner Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_num += 1

# After the loop release the cap object
video_cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
