import cv2
import numpy as np

class BoardTracker:
    def __init__(self):
        self.corner_queue = []
        self.set_dimensions()

    def set_dimensions(self, board_x=19, board_y=19, border_padding=0):
        self.dimensions = (board_y, board_x)  # numpy order
        self.padding = border_padding
        self.state = [[0]*board_x for x in range(board_y)]

    def update(self, frame):
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        board_mask = generate_board_mask(frame_HSV)
        frame_mask_blur = cv2.blur(board_mask, (3,3))

        self._update_board_corners(frame_mask_blur)

        frame_birds_eye = BoardTracker.get_frame_birds_eye(frame, self.get_corner_estimate())
        frame_debug = self._update_board_state_estimate(frame_birds_eye)

        return frame_debug

    def _update_board_corners(self, frame_mask_blur):
        # Detect edges using Canny
        threshold = 250
        canny_output = cv2.Canny(frame_mask_blur, threshold, threshold * 3)

        # Find contours
        contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_longest = max(contours, key=lambda x: cv2.arcLength(x, True))
        contour_approx = cv2.approxPolyDP(contour_longest, cv2.arcLength(contour_longest, True) * 0.03, True)

        # Find the convex hull object for each contour
        contour_hull = cv2.convexHull(contour_approx)

        if len(contour_hull) == 4:
            self.corner_queue.append(contour_hull)
            if len(self.corner_queue) > 30:
                self.corner_queue.pop(0)

    def _update_board_state_estimate(self, frame_birds_eye):
        border_px = 26 # TODO: Make proportion to be res independent
        inner = (frame_birds_eye.shape[0] - border_px,
                 frame_birds_eye.shape[1] - border_px)

        frame_debug = np.zeros(shape=frame_birds_eye.shape, dtype=frame_birds_eye.dtype)
        frame_blur = cv2.blur(frame_birds_eye, (13,13))
        frame_blur_hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)

        denoise_decay = 1
        denoise_increase = 2
        denoise_threshold = 10
        denoise_max_confidence = 50

        # Reduce confidence in current state over time
        for y, row in enumerate(self.state):
            for x, t in enumerate(row):
                if t > 0: self.state[y][x] = t - denoise_decay
                elif t < 0: self.state[y][x] = t + denoise_decay

        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                py = int(y * (inner[0] / self.dimensions[0])) + border_px
                px = int(x * (inner[1] / self.dimensions[1])) + border_px
                # Not sure why I need to convert these to int
                color = frame_blur_hsv[py,px]
                color = (int(color[0]), int(color[1]), int(color[2]))
                # See if this represents a piece
                if color[2] < 55:     # BLACK PIECE
                    self.state[y][x] = min(
                            self.state[y][x] + denoise_increase,
                            denoise_max_confidence)
                elif color[2] > 200 and color[1] < 60:  # WHITE PIECE
                    self.state[y][x] = max(
                            self.state[y][x] - denoise_increase,
                            -denoise_max_confidence)

                if self.state[y][x] > denoise_threshold:
                    color = (0,0,0)
                elif self.state[y][x] < -denoise_threshold:
                    color = (256,256,256)
                else:
                    color = (128,128,128)
                cv2.rectangle(frame_blur, (px-10,py-10),(px+10,py+10),color,-1)

        # Returns frame with debug info
        return frame_blur

    @staticmethod
    def get_frame_birds_eye(frame, corner_estimate):
        """Uses the current corner estimate to transform the board to top-down"""
        out_w, out_h = 640, 640
        src = np.float32(corner_estimate)
        dest = np.float32([[out_w, 0], [out_w, out_h], [0, out_h], [0, 0]])
        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(src, dest)
        result = cv2.warpPerspective(frame, matrix, (out_w, out_h))
        return result

    def get_corner_estimate(self):
        avg_corner_hull = sum(self.corner_queue) / len(self.corner_queue)
        return avg_corner_hull

    def get_board_state_estimate(self):
        pass

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
