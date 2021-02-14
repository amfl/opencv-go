# OpenCV-Go

## Usage

```bash
python3 main.py <VIDEO_FILE_OR_DEVICE_NUM>
```

Examples:

```bash
python3 main.py 0              # Opens video device 0
python3 main.py /foo/bar.mkv   # Opens a video file
```

## Thoughts

Random thoughts on how to track a Go board

- Figure out roughly where the board is based on color, get convex hull
    - <https://docs.opencv.org/master/d7/d1d/tutorial_hull.html>
- Obtain matrix from hull which maps some abstract grid onto board
    - find homography?
- Downres image pretty hard
- Sample pixel color at transformed grid point

- k-means clustering for board/black/white on blurred image?
  Chop up image such that every pixel is clearly one of three categories!
    https://docs.opencv.org/master/d1/d5c/tutorial_py_kmeans_opencv.html
    https://nrsyed.com/2018/03/29/image-segmentation-via-k-means-clustering-with-opencv-python/  <- This in particular looks good
