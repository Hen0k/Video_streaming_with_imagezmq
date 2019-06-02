#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 22:03:04 2019

@author: henok
"""

# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time

sender = imagezmq.ImageSender(connect_to="tcp://127.0.0.1:5555")


# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)
 
while True:
	# read the frame from the camera and send it to the server
	frame = vs.read()
	sender.send_image(rpiName, frame)