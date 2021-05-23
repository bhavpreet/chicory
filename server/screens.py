#!/usr/bin/env python3
import cv2
import np
from PIL import Image
from moon_phases import DIMENSIONS, img_to_eink_hex

font = cv2.FONT_HERSHEY_PLAIN
fontSize = 0.9

##
# code to generate the default screens

def first_boot():
    w = DIMENSIONS[0]
    h = DIMENSIONS[1]

    frameBuf = np.zeros((h,w,3), np.uint8)

    cv2.putText(
        frameBuf, #numpy array on which text is written
        "Connect to:", #text
        (5, 20), #position at which writing has to start
        font, #font family
        fontSize, #font size
        (255, 255, 255, 255), #font color
        1) #font stroke

    cv2.putText(
        frameBuf, #numpy array on which text is written
        "SSID: Chakuri", #text
        (5, 50), #position at which writing has to start
        font, #font family
        fontSize, #font size
        (255, 255, 255, 255), #font color
        1) #font stroke

    cv2.putText(
        frameBuf, #numpy array on which text is written
        "Password: 12345678", #text
        (5, 65), #position at which writing has to start
        font, #font family
        fontSize, #font size
        (255, 255, 255, 255), #font color
        1) #font stroke
    
    cv2.putText(
        frameBuf, #numpy array on which text is written
        "URL: http://192.168.4.1", #text
        (5, 80), #position at which writing has to start
        font, #font family
        fontSize, #font size
        (255, 255, 255, 255), #font color
        1) #font stroke

    Image.fromarray(frameBuf).show()
    frameBuf = cv2.rotate(frameBuf, cv2.cv2.ROTATE_90_CLOCKWISE)
    frameBuf = np.asarray(Image.fromarray(frameBuf).convert('1')).astype(int)
    frameBuf = img_to_eink_hex(frameBuf)
    frame_r = np.zeros((h,w,3), np.uint8)
    frame_r.fill(255)
    frame_r = cv2.rotate(frame_r, cv2.cv2.ROTATE_90_CLOCKWISE)
    frame_r = img_to_eink_hex(frame_r)
    return frameBuf, frame_r
    
if __name__ == '__main__':
    first_boot()

