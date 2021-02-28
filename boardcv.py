import cv2
import numpy as np

EMPTY = 0
BLACK = 1
WHITE = 2
NUM_CELL_STATES = 3


class BoardTracker:
    def __init__(self):
        self.corner_queue = []
        self.set_dimensions()

    def set_dimensions(self, board_x=19, board_y=19, border_padding=0):
        self.dimensions = (board_y, board_x)  # numpy order
        self.padding = border_padding

        # BOARD STATE
        # Stores the probabilistic board state in a 3 dimensional array.
        # - First 2 dims are just (x, y) coords on board
        # - Last dim is a vector representing which piece is there
        #   eg  [0.13, 0.02, 0.85]
        #       Means that we're pretty sure this is a white piece
        #       (Small possibility it might be empty instead)
        # Array is not normalized. The largest value wins.
        self.state = np.zeros(shape=(board_y, board_x, NUM_CELL_STATES))

    def update(self, frame):
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        board_mask = generate_board_mask(frame_HSV)
        frame_mask_blur = cv2.blur(board_mask, (3, 3))

        self._update_board_corners(frame_mask_blur)

        frame_birds_eye = BoardTracker.get_frame_birds_eye(
                frame,
                self.get_corner_estimate())
        frame_debug = self._update_board_state_estimate(frame_birds_eye)

        return frame_debug

    def _update_board_corners(self, frame_mask_blur):
        # Detect edges using Canny
        threshold = 250
        canny_output = cv2.Canny(frame_mask_blur, threshold, threshold * 3)

        # Find contours
        contours, hierarchy = cv2.findContours(
                canny_output,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

        contour_longest = max(contours, key=lambda x: cv2.arcLength(x, True))
        contour_approx = cv2.approxPolyDP(
                contour_longest,
                cv2.arcLength(contour_longest, True) * 0.03,
                True)

        # Find the convex hull object for each contour
        contour_hull = cv2.convexHull(contour_approx)

        if len(contour_hull) == 4:
            self.corner_queue.append(contour_hull)
            if len(self.corner_queue) > 30:
                self.corner_queue.pop(0)

    def _update_board_state_estimate(self, frame_birds_eye):
        border_px = 26  # TODO: Make proportion to be res independent
        inner = (frame_birds_eye.shape[0] - border_px,
                 frame_birds_eye.shape[1] - border_px)

        frame_blur = cv2.blur(frame_birds_eye, (13, 13))
        frame_blur_hsv = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2HSV)

        # Construct a new state object just from this frame.
        frame_state = np.zeros(shape=(
            self.dimensions[0], self.dimensions[1], NUM_CELL_STATES))

        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                py = int(y * (inner[0] / self.dimensions[0])) + border_px
                px = int(x * (inner[1] / self.dimensions[1])) + border_px
                # Not sure why I need to convert these to int
                color = frame_blur_hsv[py, px]
                color = (int(color[0]), int(color[1]), int(color[2]))

                # Figure out which cell state this color corresponds to
                if color[2] < 55:
                    frame_state[y, x, BLACK] = 1
                elif color[2] > 200 and color[1] < 60:
                    frame_state[y, x, WHITE] = 1
                else:
                    # Arrived at this value experimentally :)
                    # Seems to give better results than 1
                    # (Less false negatives when pieces are briefly occluded)
                    frame_state[y, x, EMPTY] = 0.5

        # Dribble the frame state into the accumulated state
        self.state = self.state * 0.95 + frame_state * 0.05

        BoardTracker.draw_debug_state(frame_blur, self.state)

        # Returns frame with debug info
        return frame_blur

    @staticmethod
    def draw_debug_state(frame, state):
        border_px = 26  # TODO: Make proportion to be res independent
        inner = (frame.shape[0] - border_px,
                 frame.shape[1] - border_px)

        cell_state = np.argmax(state, 2)

        for y in range(state.shape[0]):
            for x in range(state.shape[1]):
                py = int(y * (inner[0] / state.shape[0])) + border_px
                px = int(x * (inner[1] / state.shape[1])) + border_px

                # DRAW ON THE DEBUG IMAGE
                if cell_state[y, x] == BLACK:
                    color = (0, 0, 0)
                elif cell_state[y, x] == WHITE:
                    color = (256, 256, 256)
                else:
                    color = (128, 128, 128)
                cv2.rectangle(
                        frame,
                        (px-10, py-10),
                        (px+10, py+10),
                        color,
                        -1)

    @staticmethod
    def get_frame_birds_eye(frame, corner_estimate):
        """Uses the current corner estimate to transform the board to
        top-down"""
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
        # hard-coded values for test data
        # return np.float32(
        #         [[920.7, 90.6 ],
        #          [942.5, 615.7],
        #          [384.6, 597.7],
        #          [440.6, 50.2 ]])

    def get_board_state_estimate(self):
        return np.argmax(self.state, 2)


def generate_board_mask(frame_hsv):
    """Isolates the rough shape of the board by color matching.
    Returns the biggest group of connected pixels that is roughly the color of
    the board.
    This mask probably doesn't need to be generated every frame."""
    lower = (8, 0, 0)  # H,S,V
    upper = (64, 255, 255)
    mask = cv2.inRange(frame_hsv, lower, upper)

    # Erode/Dilate to remove noise
    kernel_3 = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(mask, kernel_3, iterations=1)
    dilation = cv2.dilate(erosion, kernel_3, iterations=3)
    return dilation
