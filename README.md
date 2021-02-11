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

- Obtain matrix which maps some abstract grid onto board
- Downres image pretty hard
- Sample pixel color at transformed grid point
