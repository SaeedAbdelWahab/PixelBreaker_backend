from ssocr import *
from ImageProject import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse


preprocess('addad1.jpg')
x ,y = detect_digits('test.bmp')
print (x[0])
cv2.imshow('test',y)
cv2.waitKey(0)
