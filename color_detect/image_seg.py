import xml.dom.minidom
import numpy as np
from PIL import Image 
from PIL import ImageDraw
import os
import cv2

xml_file = 'D:/data/20200327  (291 - 350)/20200310 CityU VVS2 SI1 SI2 (D)/20200310 CityU VVS2 SI1 SI2 (D).xml'

file_path = 'D:/a_RGB_folder_abs'
g = os.walk(file_path)

def mkdir(path):
 
	folder = os.path.exists(path)
 
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("--- new folder...  ---")
		print("---  OK  ---")
	else:
		print("---  There is this folder!  ---")
        
save_folder = file_path+'/Ruo'
mkdir(save_folder)

dom = xml.dom.minidom.parse(xml_file)
root = dom.documentElement
images = root.getElementsByTagName('image')

i = 7
t = images[i]
t_name = t.getAttribute("name")
t_width = t.getAttribute("width")
t_height = t.getAttribute("height")

img_file_path = 'D:/data/20200327  (291 - 350)/20200310 CityU VVS2 SI1 SI2 (D)/'+t_name
img = Image.open(img_file_path)
Img = cv2.imread(img_file_path)

#t_img = img
t_img = Image.new('RGB', (int(t_width), int(t_height)))
draw = ImageDraw.Draw(t_img)

t_polygon = t.getElementsByTagName("polygon")
k = 1

for t_plg in t_polygon:
 t_plg_points = t_plg.getAttribute("points")
 t_plg_points = t_plg_points.split(";")
 t_plg_points = np.asarray([[int(float(b)) for b in a.split(",")] for a in t_plg_points])
 t_x = t_plg_points[:,0]
 t_y = t_plg_points[:,1]
 txy = [(x,y) for x,y in zip(t_x,t_y)]
 t_xy = np.array(txy)
 # if 'Reflection' in t_plg.getAttribute("label"):
 #   draw.polygon(txy,fill='red')
 # else:
 #   draw.polygon(txy,fill='blue')
 rect = cv2.boundingRect(t_xy)
 a,b,c,d = rect
 croped = Img[b:b+d, a:a+c].copy()
 t_xy = t_xy - t_xy.min(axis=0)
 mask = np.zeros(croped.shape[:2], np.uint8)

 cv2.drawContours(mask, [t_xy], -1, (255, 255, 255), -1, cv2.LINE_AA)
 dst = cv2.bitwise_and(croped, croped, mask = mask)
 bg = np.ones_like(croped, np.uint8)*255
 dst2 = bg + dst
 cv2.bitwise_not(bg, bg, mask = mask)
 path = os.path.join
 window_name = 'image'
 if 'Reflection' in t_plg.getAttribute("label"):
  cv2.imwrite('D:/a_RGB_folder_abs/Ruo/redst_%d.png'%(k), dst)
 else:
  cv2.imwrite('D:/a_RGB_folder_abs/Ruo/dst_%d.png'%(k), dst) 
 # cv2.imwrite('D:/data/Ruoning/dst2_%d.png'%(k), dst2)
 # cv2.imshow(window_name, dst)
 # cv2.imshow(window_name, dst2)
 cv2.waitKey(0)
 t_plg_label = t_plg.getAttribute("label")
 t_plg_occluded = t_plg.getAttribute("occluded")
 k += 1

# t_img.save(os.path.join(save_folder,t_name[:15]+'_mask.png'))
print(i,t_name[:15] + ' saved ...')
i=i+1