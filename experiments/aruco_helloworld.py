import cv2
import numpy as np
import pickle
import sys

# Set PYTHONPATH to include the repo root to make this work
import vidio

def construct_example_objectpoints():
    """Return a map of id to object-space coordinates. Suitable for constructing arguments for solvePnP or projectpoints.

    {id: [x,y,0]}
    """
    # List of IDs as printed on pdf
    ids = [388,201,234,116,596,681,11,220,169,85,415,137,923,735,84,191,393,996,104,557,721,7,880,746,493,115,746,476,631,191,212,826,582,62,341]

    return { v:[float(i%5),float(i//5),0.0] for i,v in enumerate(ids) }

def get_camera_matrix(filename):
    """Read the camera matrix from a file.
    Generated by calibrate_camera.py in the experiments dir."""

    with open(filename, 'br') as f:
        return pickle.loads(f.read())

    # Hard-coded test data
    # return [[977.4105363    0.         710.85510632],
    #         [  0.         948.47764572 382.80313717],
    #         [  0.           0.           1.        ]]

def main(video_device, camera_matrix_file):
    video_cap = vidio.get_video_cap(video_device)
    camera_matrix = get_camera_matrix(camera_matrix_file)

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

            if len(corners) >= 6:
                ### solvePnP to get camera pose
                # Get imagepoints from corners
                # Get objectpoints based on whichever imagepoints are observed
                # We already have the cameraMatrix
                witnessed_objectpoints = np.array([example_objectpoints[aruco_id[0]] for aruco_id in ids])
                witnessed_imagepoints = np.array([c[0][0] for c in corners])

                # print(witnessed_objectpoints)
                # print(witnessed_imagepoints)
                # print(camera_matrix)

                # For each identified imagepoint,
                # we should know where it is in object space.
                assert(len(witnessed_imagepoints) == len(witnessed_objectpoints))

                retval, rvec, tvec = cv2.solvePnP(witnessed_objectpoints,
                                                  witnessed_imagepoints,
                                                  camera_matrix,
                                                  None)

                ### projectpoints to get board dimensions
                # Calculate objectPoints of board

                novel_objectpoints = np.array([
                    [3.5, 3.5, 0.0],
                    [0.0, 0.0, 0.0],
                    [0.0, 6.0, 0.0],
                    [4.0, 0.0, 0.0],
                    [4.0, 6.0, 0.0],
                ])
                novel_imagepoints, jacobian = cv2.projectPoints(
                        novel_objectpoints,
                        rvec, tvec,
                        camera_matrix,
                        None)

                print(novel_imagepoints)

                for p in witnessed_imagepoints:
                    cv2.circle(frame,
                               (int(p[0]), int(p[1])),
                               6,
                               (0,255,255),
                               -1)

                for p in novel_imagepoints:
                    p = p[0]
                    cv2.circle(frame,
                               (int(p[0]), int(p[1])),
                               6,
                               (0,0,255),
                               -1)

        ####################################

        cv2.imshow("Program Output", frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

        num_frames += 1

    # After the loop release the cap object
    video_cap.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_device = sys.argv[1]
    camera_matrix_file = sys.argv[2]

    main(video_device, camera_matrix_file)
