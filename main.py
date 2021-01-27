import cv2

video_capture_device_index = 2
webcam = cv2.VideoCapture(video_capture_device_index)

ret, video_frame = webcam.read()

print(video_frame)

frame_width = int(round(webcam.get(cv2.CAP_PROP_FRAME_WIDTH)))
frame_height = int(round(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print(frame_width, frame_height)

#########################

cv2.imshow("Butts", video_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
