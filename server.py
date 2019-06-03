#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 22:15:58 2019

@author: henok
"""

# import the necessary packages
from imutils.video import VideoStream
import imagezmq
import socket
import time
import cv2

def initSender(out_port=5050):
    frameSender = imagezmq.ImageSender(connect_to="tcp://127.0.0.1:%d" % out_port)
    senderName = socket.gethostname()

    return frameSender, senderName

def startCapture(delay=2.0):
    print("getting camera")
    # here src=2 is for my usb webcam. yours can be 1 or 2 or 3 and so on for usb
    # and 0 or -1 for built in webcam
    videoStream = VideoStream(src=2).start()
    print("got camera")
    time.sleep(delay)

    return videoStream

def sendframe(sender, vs, name):
    frame = vs.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sender.send_image(name, frame)
    print(frame.shape)
    return 0

def initReciver(in_port=5051):    
    # initialize the ImageHub object
    imageHub = imagezmq.ImageHub(open_port='tcp://127.0.0.1:%d' %in_port)

    return imageHub

def reciveandshow(hub):
    # receive sender host name and frame from the sender
    # and acknowledge the receiption
    (rpiName, frame) = hub.recv_image()
    hub.send_reply(b'OK')
    
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('From %s (client)' % rpiName, frame)
	
    c = cv2.waitKey(1)
    if c == 27:
        return -1

    return 0


# Sending
frameSender, senderName = initSender()
vs = startCapture()




# video streaming over network with OpenCV and ImageZMQPython
frameHub = initReciver()

while True:
    #Reciving
    reciveandshow(frameHub)

    # Sending
    sendframe(frameSender, vs, senderName)
