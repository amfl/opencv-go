import numpy as np
import cv2 as cv
import glob

dims = (6,9)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((dims[0] * dims[1],3), np.float32)
objp[:,:2] = np.mgrid[0:dims[0],0:dims[1]].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('calibration_images/*.jpg')
for fname in images:
    print(fname)
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, dims, None)
    print("Scanned")
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("ret is true")
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, dims, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
cv.destroyAllWindows()

###############################

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
if ret:
    print("=== Matrix ===")
    print(mtx)
    print("=== Dist ===")
    print(dist)
    print("=== Rvecs ===")
    print(rvecs)
    print("=== Tvecs ===")
    print(tvecs)
