#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 22:15:58 2019

@author: henok
"""

# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2


# initialize the ImageHub object
imageHub = imagezmq.ImageHub()


# video streaming over network with OpenCV and ImageZMQPython

# start looping over all the frames
while True:
	# receive RPi name and frame from the RPi and acknowledge
	# the receipt
    (rpiName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('From %s' % rpiName, frame)
	
    c = cv2.waitKey(1)
    if c == 27:
        break

