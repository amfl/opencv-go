import cv2

def get_video_cap(video_source):
    try:
        video_source = int(video_source)
    except:
        # Ignore error - We're likely being passed a filename.
        pass
    video_cap = cv2.VideoCapture(video_source)

    frame_width = int(round(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    frame_height = int(round(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(frame_width, frame_height)

    return video_cap
