# bitrate-viewer
Plots a graph showing the variation of the bitrate as well as up to 75 I-Frames throughout your video. The average bitrate is shown on the legend. In addition to this, the minimum, maximum and standard deviation is shown above the graph. See the example below:



![Example Graph](https://github.com/InB4DevOps/bitrate-viewer/blob/main/bitrate_graph.png?raw=true)

# Requirements:
- Python **3.6+**
- `pip install -r requirements.txt`
- FFprobe in your PATH.

# Usage
```
usage: main.py [-h] -i INPUT_VIDEO_PATH [INPUT_VIDEO_PATH ...] [-f {xml,json}] [-o OUTPUT_FILENAME] [-t TITLE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_VIDEO_PATH [INPUT_VIDEO_PATH ...], --input-video-path INPUT_VIDEO_PATH [INPUT_VIDEO_PATH ...]
                        Enter one or more paths of input videos. Relative or absolute paths are supported.
  -f {xml,json}, --output-format {xml,json}
                        Specify the output format for the file written by FFProbe. (default: 'xml')
  -o OUTPUT_FILENAME, --output-filename OUTPUT_FILENAME
                        Optional output image filename without extension. If not provided, for single input the video stem is used; for multiple inputs 'comparison' is used.
  -t TITLE, --title TITLE
                        Optional custom title for the graph. If omitted, uses the filename(s) by default.
```

Single file example:

`python main.py -i video.mp4 -f json`

This forces FFprobe to write its output in JSON (default is XML) and saves it as <video_file_name>.json.
The graph will be saved as <video_file_name>.png.

Multiple files comparison example:

`python main.py -i a.mp4 b.webm c.mov`

This will analyze all three files and create a single comparison graph `comparison.png` with three lines (one per file) labeled with filename, codec, and average bitrate. Sidecar FFprobe outputs will be saved alongside as `a.json|xml`, `b.json|xml`, etc., depending on `-f`.

Special thanks to [@CrypticSignal]( https://github.com/CrypticSignal ) for helping me along the way.
