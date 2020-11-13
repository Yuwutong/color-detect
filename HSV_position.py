import math
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt


pic_file = 'D:/css/color_detect/dst_3BIG.jpg'

img_bgr = cv2.imread(pic_file, cv2.IMREAD_COLOR) #OpenCV读取颜色顺序：BRG 
img_b = img_bgr[..., 0]
img_g = img_bgr[..., 1]
img_r = img_bgr[..., 2]

img_r, img_g, img_b = img_r/255.0, img_g/255.0, img_b/255.0

[rows, cols] = img_r.shape
mx = np.mat(np.zeros((rows,cols)))
mn = np.mat(np.zeros((rows,cols)))
df = np.mat(np.zeros((rows,cols)))
h = np.mat(np.zeros((rows,cols)))
s = np.mat(np.zeros((rows,cols)))
v = np.mat(np.zeros((rows,cols)))

for i in range(rows):
    for j in range(cols):
        mx[i,j] = max(img_r[i,j], img_g[i,j], img_b[i,j])
        mn[i,j] = min(img_r[i,j], img_g[i,j], img_b[i,j])
        df[i,j] = mx[i,j] - mn[i,j]
        if mx[i,j] == mn[i,j] :
            h[i,j]  = 0
        elif mx[i,j]  == img_r[i,j] and img_g[i,j] >= img_b[i,j]:
            h[i,j]  = (60 * ((img_g[i,j]-img_b[i,j])/df[i,j]) + 0) % 360
        elif mx[i,j]  == img_r[i,j] and img_g[i,j] < img_b[i,j]:
            h[i,j]  = (60 * ((img_g[i,j]-img_b[i,j])/df[i,j]) + 360) % 360    
        elif mx[i,j] == img_g[i,j]:
            h[i,j] = (60 * ((img_b[i,j]-img_r[i,j])/df[i,j]) + 120) % 360
        elif mx[i,j] == img_b[i,j]:
            h[i,j] = (60 * ((img_r[i,j]-img_g[i,j])/df[i,j]) + 240) % 360
        if mx[i,j] == 0:
            s[i,j] = 0
        else:
            s[i,j] = df[i,j]/mx[i,j]
            v[i,j] = mx[i,j]
            
plt.hist(h,facecolor="red", edgecolor="red")
plt.show()
plt.hist(s,facecolor="green", edgecolor="green")
plt.show()
plt.hist(v,facecolor="blue", edgecolor="blue")
plt.show()


# h_hist = cv2.calcHist([img_bgr], [0], None, [360], [0, 360])
# s_hist = cv2.calcHist([img_bgr], [1], None, [360], [0, 1])
# v_hist = cv2.calcHist([img_bgr], [2], None, [360], [0, 1])

# plt.plot(h, label='H', color='blue')
# plt.legend(loc='best')
# plt.xlim([0, 180])
# plt.show()

# plt.plot(s, label='S', color='green')
# plt.legend(loc='best')
# plt.xlim([0, 255])
# plt.show()


# plt.plot(v, label='V', color='red')
# plt.legend(loc='best')
# plt.xlim([0, 255])
# plt.show()













