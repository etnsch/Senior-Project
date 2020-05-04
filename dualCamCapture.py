import os
import time
from datetime import datetime
import picamera
from picamera import PiCamera
import cv2
import numpy as np


def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)
    out_min = 0.0
    out_max = 255

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out


# Settings
countdown = 1  # Interval between image captures (seconds)
cam_width = 1280  # Cam sensor width
cam_height = 480  # Cam sensor height

scale_ratio = 0.5

# Camera resolution height must be dividable by 16, and width by 32
cam_width = int((cam_width + 31) / 32) * 32
cam_height = int((cam_height + 15) / 16) * 16
print("Used camera resolution: " + str(cam_width) + " x " + str(cam_height))

# Buffer for captured image settings
img_width = int(cam_width * scale_ratio)
img_height = int(cam_height * scale_ratio)
capture = np.zeros((img_height, img_width, 4), dtype=np.uint8)
print("Scaled image resolution: " + str(img_width) + " x " + str(img_height))

# Initialize camera
camera = PiCamera(stereo_mode='side-by-side', stereo_decimate=False)
camera.resolution = (cam_width, cam_height)
camera.framerate = 20
camera.hflip = False

counter = 0
t2 = datetime.now()
print("Starting photo sequence")
for frame in camera.capture_continuous(capture, format="bgra", use_video_port=True, resize=(img_width, img_height)):
    t1 = datetime.now()
    cntdwn_timer = countdown - int((t1 - t2).total_seconds())

    # If cowntdown is zero -> record next image
    if cntdwn_timer == -1:
        counter += 1

        # Save raw image
        cv2.imwrite('raw' + str(counter) + '.png', frame)

        # Split image to left and right
        imgLeft = frame[0:240, 0:320]
        imgRight = frame[0:240, 320:640]
        leftName = str(counter) + 'nir.png'
        rightName = str(counter) + 'r.png')
        cv2.imwrite(leftName, imgLeft)
        cv2.imwrite(rightName, imgRight)

        # Split left & right into components
        b, g, nir, a = cv2.split(imgLeft)
        b1, g1, r, a1 = cv2.split(imgRight)

        # Calculate NDVI
        bottom = (nir.astype(float) + r.astype(float))
        bottom[bottom == 0] = 0.01
        ndvi = (nir.astype(float) - r) / bottom
        ndvi = contrast_stretch(ndvi)
        ndvi = ndvi.astype(np.uint8)
        ndvi = cv2.applyColorMap(ndvi, cv2.COLORMAP_JET)
        cv2.imwrite('ndvi' + str(counter) + '.png', ndvi)

        # Calculate Chlorophyll Index
        b1 = g1.astype(float)
        b1[b1 == 0] = 0.01
        ci = nir.astype(float) / b1
        ci = contrast_stretch(ci)
        ci = ci.astype(np.uint8)
        ci = cv2.applyColorMap(ci, cv2.COLORMAP_SUMMER)
        cv2.imwrite('ci' + str(counter) + '.png', ci)

        t2 = datetime.now()
        time.sleep(1)
        cntdwn_timer = 0
        next

        key = cv2.waitKey(1)

        # Press q to quit
        if (key == ord("q")):
            break

    print("Photo sequence finished")