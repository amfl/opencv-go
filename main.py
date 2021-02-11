import cv2
import sys

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

    # print(video_frame)

while True:
    ret, frame = video_cap.read()

    #########################

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 50)

    for corner in corners:
        x,y= corner[0]
        x= int(x)
        y= int(y)
        cv2.rectangle(frame, (x-10,y-10),(x+10,y+10),(255,0,0),-1)

    cv2.imshow("goodFeaturesToTrack Corner Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
video_cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
