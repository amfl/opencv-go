# Aruco Helloworld

Goals:

- Detect aruco markers
- Use many predefined locations (provided by the aruco markers) to inform an estimation of a known location
    - <https://answers.opencv.org/question/189278/aruco-markers-point-position-estimation/>
    - Can I do this with <https://www.pythonpool.com/opencv-solvepnp/>? I think so. Object points are 3d, but we can set one axis to 0s.
    - <https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html>

Usage:

```bash
cd $REPO_ROOT
export PYTHONPATH=$(pwd)
# Generate camera matrices (You will need your own calibration images)
python3 experiments/calibrate_camera.py
# Run the code (You will need your own camera/footage)
python3 experiments/aruco_helloworld.py input/testdata/aruco2.mkv input/camera.cmat input/distortion.cmat
```

Specifics:

```
cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs[, rvec[, tvec[, useExtrinsicGuess[, flags]]]]) → retval, rvec, tvec
```

**tl;dr**: Given some known point relationships (objectPoints) and their observed position (imagePoints), we want to estimate the location of some unobserved point(s) on the image (novelImagePoints).

- <https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html> -> cameraMatrix
- (objectPoints, imagePoints, cameraMatrix) -> `solvePnP` -> (rvec, tvec)
    - <http://www.opencv.org.cn/opencvdoc/2.3.2/html/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html?highlight=findfun#solvepnp>
- (novelObjectPoints, rvec, tvec) -> `projectpoints` -> novelImagePoints
    - <http://www.opencv.org.cn/opencvdoc/2.3.2/html/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html?highlight=findfun#projectpoints>
