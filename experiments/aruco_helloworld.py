import cv2
import sys
import numpy as np

# Set PYTHONPATH to include the repo root to make this work
import vidio


def main():
    video_source = sys.argv[1]
    video_cap = vidio.get_video_cap(video_source)

    num_frames = 0  # frame counter
    frame_debug = None

    while True:
        ret, frame = video_cap.read()

        ####################################
        # STUFF HAPPENS HERE!
        ####################################

        # if num_frames % 10 == 0:  # TODO: Do this per time rather than frames
        # Detect the board
        # frame_debug = tracker.update(frame)

        arucoParams = cv2.aruco.DetectorParameters_create()
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(
                frame,
                arucoDict,
                parameters=arucoParams)

        for i in range(len(corners)):  # Iterate through each marker

            points = np.array(corners[i][0], dtype=np.int32)

            # Draw the bounds of the aruco marker
            color = (0, 0, 256)
            cv2.polylines(frame,
                          [points],
                          True,
                          color,
                          2)

            # Draw ID onto the image
            text = str(ids[i][0])
            text_pos = points[0]
            text_color = (0, 128, 0)
            # print(text)
            cv2.putText(frame,
                        text,
                        text_pos,
                        cv2.FONT_HERSHEY_PLAIN,
                        1,
                        text_color)

        ####################################

        cv2.imshow("Program Output", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        num_frames += 1

    # After the loop release the cap object
    video_cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
