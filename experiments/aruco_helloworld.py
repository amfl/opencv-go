import cv2
import sys
import numpy as np

# Set PYTHONPATH to include the repo root to make this work
import vidio

def construct_example_objectpoints():
    """Return a map of id to object-space coordinates. Suitable for constructing arguments for solvePnP or projectpoints.

    {id: (x,y,0)}
    """
    # List of IDs as printed on pdf
    ids = [388,201,234,116,596,681,11,220,169,85,415,137,923,735,84,191,393,996,104,557,721,7,880,746,493,115,746,476,631,191,212,826,582,62,341]

    return { v:(i%5,i//5,0) for i,v in enumerate(ids) }

def main():
    video_source = sys.argv[1]
    video_cap = vidio.get_video_cap(video_source)

    num_frames = 0  # frame counter
    frame_debug = None

    example_objectpoints = construct_example_objectpoints()

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

        if ids is not None:
            witnessed_objectpoints = [example_objectpoints[aruco_id[0]] for aruco_id in ids]
            print(witnessed_objectpoints)

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
