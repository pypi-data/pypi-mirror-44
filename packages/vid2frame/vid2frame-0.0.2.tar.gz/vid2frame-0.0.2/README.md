# vid2frame
vid2frame is built on top of opencv-python. It converts video into frames

## Python version
Python 3.6.4

## Dependencies
  1. opencv-python
  2. numpy

## How to install
vid2frame has been published on Python Package Index (PyPi). vid2frame can be installed using the following command.
```
pip install vid2frame
```

## How to use
```
from vid2frame import vid2frame

vid2frame.convert('test.mp4', 'target_folder')
```
The convert function will read `test.mp4` and store the frames to `target_folder`