import sys
import capture
import opencv_ocr

# capture.capture()

# Use command-line argument if provided, else use default
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "captures/hello.png"

print(opencv_ocr.opencv_ocr(filename))