import pandas as pd
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt



img = cv2.imread('D:/css/color_detect/dst_2BIG.jpg')
img_bgr = img
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
            
def get_color_name(r, g, b):
    min_diff = 10000
    color_name = ''
    for i in range(len(csv_df)):
        d = abs(r - int(csv_df.loc[i, "R"])) + abs(g - int(csv_df.loc[i, "G"]))+ abs(b - int(csv_df.loc[i, "B"]))
        if d <= min_diff:
            min_diff = d
            color_name = csv_df.loc[i,"color_name"]
    return color_name


def click_info(event, x, y, flags, param):
    # 只处理双击事件
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global H,S,V,b,g,r,xpos,ypos, clicked
        xpos = x
        ypos = y
        b, g, r = img[y, x]     # 获取b, g, r
        b = int(b)
        g = int(g)
        r = int(r)
        H = int(h[y,x])
        S = round(s[y,x],2)
        V = round(v[y,x],2)
        clicked = True


H = S = V = r = g = b = xpos = ypos = 0
clicked = False

index = ["color", "color_name", "hex", "R", "G", "B"]
csv_df = pd.read_csv('D:/css/color_detect/colors.csv', names=index, header=None)

cv2.namedWindow('image')
cv2.setMouseCallback('image',  click_info)

while True:
    cv2.imshow("image", img)
    if clicked:
        # 绘制显示文字的区域
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = get_color_name(r, g, b) + ' H='+ str(H) +  ' S='+ str(S) + ' V='+ str(V)
        # 显示文字内容
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # 如果像素点的颜色太偏向于白色,就用黑色来显示文字
        if(r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    clicked=False
    # 点击 esc键
    if cv2.waitKey(20) & 0xFF ==27:
        break

cv2.destroyAllWindows()
