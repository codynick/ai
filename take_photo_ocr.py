#!/usr/bin/env python3
import cv2, time, os

# --- your original code (unchanged) ---
time1 = time.time()
os.makedirs("captures", exist_ok=True)
device = "/dev/video0"
cap = cv2.VideoCapture(device, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    raise RuntimeError(f"? Cannot open camera {device}")

print("Warming up camera...")
for i in range(10):
    cap.read()
    time.sleep(0.1)

ret, frame = cap.read()
tries = 0
while (not ret or frame is None or frame.size == 0) and tries < 10:
    time.sleep(0.2)
    ret, frame = cap.read()
    tries += 1

if not ret or frame is None or frame.size == 0:
    raise RuntimeError("?? Could not capture a valid frame (camera may need replug or permission fix)")

filename = f"captures/photo_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
cv2.imwrite(filename, frame)
cap.release()
time1 = round((time.time()-time1) * 10) / 10
print(f"Photo saved to {filename} from {device},\nCapturing Time: {time1} seconds")

# --- minimal OCR add-on (new) ---
import pytesseract
import numpy as np

# Point pytesseract to tesseract binary (Ubuntu apt path)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

time1  =time.time()
img = cv2.imread(filename, cv2.IMREAD_COLOR)
if img is None or img.size == 0:
    raise RuntimeError("Could not read the saved image for OCR.")

print("Image Read Time: "+str(round((time.time()-time1) * 10) / 10))
time1  =time.time()

# keep it simple: grayscale only (no fancy preprocessing)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print("cv2.COLOR_BGR2GRAY Time: "+str(round((time.time()-time1) * 10) / 10))
time1  =time.time()

# general English text: PSM 6 = single uniform block of text (works well for documents)
# try PSM 11 (sparse text) if needed: '--psm 11'
ocr_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(gray, config=ocr_config, lang='eng')

print("\n--- OCR RESULT ---\n")
print(text.strip() if text else "")
print("\n------------------\n")
print("OCR Time: "+str(round((time.time()-time1) * 10) / 10))
