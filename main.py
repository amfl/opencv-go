import cv2
import sys
import numpy as np

import boardcv
import vidio

def main():
    video_source = sys.argv[1]
    video_cap = vidio.get_video_cap(video_source)

    frame_num = 0
    board_mask = None
    tracker = boardcv.BoardTracker()

    while True:
        ret, frame = video_cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if frame_num % 10 == 0:  # TODO: Do this per time rather than frames
            # Detect the board
            tracker.update(frame)

        # Draw onto the image

        corners = tracker.get_corner_estimate()
        cv2.drawContours(frame, [corners], -1, (255,255,255), 2)

        # Slam a marker at the board corners
        for corner in corners:
            x,y= corner[0]
            x= int(x)
            y= int(y)
            cv2.rectangle(frame, (x-10,y-10),(x+10,y+10),(0,0,255),-1)

        # Obtain a birds eye view
        out_w, out_h = 640, 640
        src = np.float32(tracker.get_corner_estimate())
        dest = np.float32([[out_w, 0], [out_w, out_h], [0, out_h], [0, 0]])
        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(src, dest)
        result = cv2.warpPerspective(frame, matrix, (out_w, out_h))

        result = tracker.draw_piece_debug(result)

        cv2.imshow("Program Output", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_num += 1

    # After the loop release the cap object
    video_cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
