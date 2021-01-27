import cv2

video_capture_device_index = 2
webcam = cv2.VideoCapture(video_capture_device_index)

while True:
    ret, video_frame = webcam.read()

    # print(video_frame)

    # frame_width = int(round(webcam.get(cv2.CAP_PROP_FRAME_WIDTH)))
    # frame_height = int(round(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # print(frame_width, frame_height)

    #########################

    img = video_frame
    gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners= cv2.goodFeaturesToTrack(gray, 100, 0.01, 50)

    for corner in corners:
        x,y= corner[0]
        x= int(x)
        y= int(y)
        cv2.rectangle(img, (x-10,y-10),(x+10,y+10),(255,0,0),-1)

    cv2.imshow("goodFeaturesToTrack Corner Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object 
webcam.release()
# Destroy all the windows 
cv2.destroyAllWindows()
