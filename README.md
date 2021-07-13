# Stream Recorder & Automatic Retrier

Usage: `python record.py <stream link> <streamer name>`

- This will attempt to record a stream and save it in `recordings/<streamer name>`

Usage: `python fix_all.py`

- This will fix all malformed streams.

Requirements: 
- Streamlink with whatever plugins are necessary for your stream
- ffmpeg in your system PATH variable.
- Python 3.5