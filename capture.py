  GNU nano 7.2                                                                                                              /home/wfudronelab/capture.py                                                                                                                        
#!/usr/bin/env python3
"""
capture_from_a6400.py
Simple helper: checks camera presence, takes one photo, and saves it to a folder with timestamp.
It uses gphoto2 CLI, so gphoto2 must be installed on the Pi.
"""

import subprocess
import os
from datetime import datetime
import sys

DOWNLOAD_DIR = "/home/wfudronelab/pi/photos"

def check_camera():
    """Return True if gphoto2 auto-detect finds a camera."""
    try:
        out = subprocess.run(["gphoto2", "--auto-detect"], capture_output=True, text=True, check=True)
        # Typical output includes header then "Model                          Port"
        # If only header or blank, no camera found.
        lines = [l for l in out.stdout.splitlines() if l.strip()]
        # keep lines after the header line "Model                          Port"
        if len(lines) >= 2:
            # we have at least one detected device
            return True, out.stdout.strip()
        return False, out.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"gphoto2 error: {e.stderr or e.stdout}"

def take_photo(download_dir=DOWNLOAD_DIR, prefix="IMG"):
    """Trigger a capture and download image to download_dir with timestamp filename."""
    os.makedirs(download_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.jpg"
    filepath = os.path.join(download_dir, filename)

    cmd = [
        "gphoto2",
        "--capture-image-and-download",
        "--filename", filepath
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
        return True, {"path": filepath, "gphoto_stdout": proc.stdout}
    except subprocess.CalledProcessError as e:
        return False, {"error": "capture failed", "returncode": e.returncode, "stdout": e.stdout, "stderr": e.stderr}
    except subprocess.TimeoutExpired:
        return False, {"error": "gphoto2 timed out"}

def main():
    ok, info = check_camera()
    if not ok:
        print("Camera not detected. gphoto2 output:")
        print(info)
        sys.exit(2)

    print("Camera detected. Taking photo...")
    ok, result = take_photo()
    if ok:
        print("Photo saved to:", result["path"])
    else:
        print("Error taking photo:", result)
        sys.exit(3)

if __name__ == "__main__":
    main()
