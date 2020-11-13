# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 22:38:12 2020

@author: mastaffs
"""


import cv2
import numpy as np
from matplotlib import pyplot as plt

pic_file = 'D:/css/HSVtest1J/dst_4BIG.png'

image=cv2.imread(pic_file)
HSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
def getpos(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print(HSV[y,x])
#th2=cv2.adaptiveThreshold(imagegray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
# cv2.imshow("imageHSV",HSV)
# cv2.imshow('image',image)
# cv2.setMouseCallback("imageHSV",getpos)
# cv2.waitKey(0)

h_hist = cv2.calcHist([HSV], [0], None, [180], [0, 180])
s_hist = cv2.calcHist([HSV], [1], None, [256], [0, 255])
v_hist = cv2.calcHist([HSV], [2], None, [256], [0, 255])
                                                
a = plt.plot(h_hist, label='H', color='blue')
plt.legend(loc='best')
plt.xlim([5, 140])
#plt.savefig('D:/css/HSVtest1J/hist_h1.png')
plt.show()


# k = cv2.waitKey(0)
# if k == ord("s"):

plt.plot(s_hist, label='S', color='green')
# plt.legend(loc='best')
# plt.xlim([5, 255])
# plt.show()


plt.plot(v_hist, label='V', color='red')
# plt.legend(loc='best')
# plt.xlim([5, 255])
# plt.show()

for n in range(0,20):
    print(n)