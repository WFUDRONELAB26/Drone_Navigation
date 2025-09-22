  GNU nano 7.2                                          /home/wfudronelab/capture.py                                              M     
#!/usr/bin/env python3
"""
capture_from_a6400.py
Capture a photo from Sony A6400 in PC Remote mode using gphoto2.
Photos are saved in sequence as img1.jpg, img2.jpg, ...
"""

import subprocess
import os
import re

# Folder where photos will be stored
DOWNLOAD_DIR = "/home/wfudronelab/pi/photos"

# Ensure the directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_next_filename(prefix="img", ext=".jpg"):
    """
    Look at existing files in DOWNLOAD_DIR and return the next available filename
    like img1.jpg, img2.jpg, ...
    """
    files = os.listdir(DOWNLOAD_DIR)
    nums = []
    for f in files:
        match = re.match(rf"{prefix}(\d+){ext}$", f)
        if match:
            nums.append(int(match.group(1)))
    next_num = max(nums) + 1 if nums else 1
    return os.path.join(DOWNLOAD_DIR, f"{prefix}{next_num}{ext}")

def take_photo():
    """
    Trigger the camera to capture and download an image to DOWNLOAD_DIR
    with the next sequential filename.
    """
    filepath = get_next_filename()
    cmd = [
        "gphoto2",
        "--capture-image-and-download",
        "--filename", filepath
    ]
    try:
        subprocess.run(cmd, check=True)
        print("✅ Photo saved to:", filepath)
    except subprocess.CalledProcessError as e:
        print("❌ Error during capture:", e)

if __name__ == "__main__":
    take_photo()

