import xml.dom.minidom
import numpy as np
from PIL import Image 
from PIL import ImageDraw
import os
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd

read_xml = 'D:/data/20200327  (291 - 350)'
g_xml = os.listdir(read_xml)
for file in g_xml:  
    xml_path = read_xml + '/' + file
    
    for path,d,filelist in os.walk(xml_path):
        for filename in filelist:
            if 'CityU' in filename:
                xml_file = xml_path + '/' + filename
                print(xml_file)
                dom = xml.dom.minidom.parse(xml_file)
                root = dom.documentElement
                images = root.getElementsByTagName('image')

                for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]:
                    t = images[i]
                    t_name = t.getAttribute("name")
                
                    img_file_path = xml_path + '/' +  t_name
                    img = Image.open(img_file_path)
                    Img = cv2.imread(img_file_path)
                
                    t_polygon = t.getElementsByTagName("polygon")
                    k = 1
                
                    file_path = 'D:/a_RGB_291_350'
                
                    def mkdir(path):
                 
                        folder = os.path.exists(path)
                 
                        if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
                            os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
                            print("--- new folder...  ---")
                            print("---  OK  ---")
                        else:
                            print("---  There is this folder!  ---")
                    
                
                    for t_plg in t_polygon:
                        t_plg_points = t_plg.getAttribute("points")
                        t_plg_points = t_plg_points.split(";")
                        t_plg_points = np.asarray([[int(float(b)) for b in a.split(",")] for a in t_plg_points])
                        t_x = t_plg_points[:,0]
                        t_y = t_plg_points[:,1]
                        txy = [(x,y) for x,y in zip(t_x,t_y)]
                        t_xy = np.array(txy)
                
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
                        if 'Crystal_Reflection' in t_plg.getAttribute("label"):
                            save_folder_Crystal = file_path+'/'+ 'Crystal' + file[-3:] + '%d'%i
                            mkdir(save_folder_Crystal)
                            cv2.imwrite(save_folder_Crystal + '/redst_%d.png'%(k), dst)
                        if 'Crystal' in t_plg.getAttribute("label"):
                            cv2.imwrite(save_folder_Crystal + '/dst_%d.png'%(k), dst)
                        if 'Pinpoint_Reflection' in t_plg.getAttribute("label"):
                            save_folder_Pinpoint = file_path+'/'+ 'Pinpoint' + file[-3:] + '%d'%i
                            mkdir(save_folder_Pinpoint)
                            cv2.imwrite(save_folder_Pinpoint + '/redst_%d.png'%(k), dst)
                        if 'Pinpoint' in t_plg.getAttribute("label"):
                            cv2.imwrite(save_folder_Pinpoint + '/dst_%d.png'%(k), dst)
                        if 'Cloud_Reflection' in t_plg.getAttribute("label"):
                            save_folder_Cloud = file_path+'/'+ 'Cloud' + file[-3:] + '%d'%i
                            mkdir(save_folder_Cloud)
                            cv2.imwrite(save_folder_Cloud + '/redst_%d.png'%(k), dst)
                        if 'Cloud' in t_plg.getAttribute("label"):
                            cv2.imwrite(save_folder_Cloud + '/dst_%d.png'%(k), dst)    
                
                        cv2.waitKey(0)
                        t_plg_label = t_plg.getAttribute("label")
                        t_plg_occluded = t_plg.getAttribute("occluded")
                        k += 1
                        
                	
                   