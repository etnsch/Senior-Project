# Multispectral Camera for Monitoring Plant Health

A senior project in computer engineering at Elizabethtown College. This project uses a dual camera system attached to a drone in order to provide insight to plant health, using normalized difference vegetation index (NDVI) and chlorophyll index (CI).

## Overview

### Hardware

This project uses a Raspberry Pi Compute Module 3+ Lite, a StereoPi PCB, a Raspberry Pi camera module v2, and a Raspberry Pi NoIR camera module v2.

### Software

The image capture and processing is performed by a python script. Still images are pulled from a continuous stream once a second to be processed and saved for analysis.

## Built With

* [StereoPi](https://stereopi.com/) - Dual camera interface board
* [OpenCV](https://opencv.org/) - Computer vision library
* [picamera](https://github.com/waveform80/picamera) - Python interface to the Raspberry Pi camera module
* [NumPy](https://numpy.org/) - Python scientific computing package

## Acknowledgments

Thanks to Dr. Peilong Li and Dr. Joseph Wunderlich, for advising and supporting this project, and for allowing the use of drone components from the Robotics and Machine Intelligence Lab.
