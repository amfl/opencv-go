# OpenCV-Go

Point a webcam at your Go board and record real games in `sgf` format.

The resulting `sgf` file could be analyzed with AI.

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
    - Use extrapolated hough lines instead of convex hull? Might work better with occluded corners, or skin tone matching board color.
- Downres image pretty hard
- Sample pixel color at transformed grid point
