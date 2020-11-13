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

#5 ##3
read_xml = 'D:/data/20200408  (351 - 410)'
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
                for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]:
                    t = images[i]
                    t_name = t.getAttribute("name")
                    file_path = 'D:/a_RGB_351_410_abs'
                
                    img_file_path = xml_path + '/' +  t_name
                    Img = cv2.imread(img_file_path)
                    save_folder = file_path+'/'+ file[-3:] + '%d'%i
                    cv2.imwrite(save_folder +'/'+t_name[:15]+'.png', Img)
                
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
                
                        a = np.array(t_xy,np.int32)
                        if 'Reflection' in t_plg.getAttribute("label"):
                            Img = cv2.polylines(Img, np.int32([a]), 1, (255,0,0),2)
                        else:
                            Img = cv2.polylines(Img, np.int32([a]), 1, (0,0,255),2)
                        t_plg_label = t_plg.getAttribute("label")
                        t_plg_occluded = t_plg.getAttribute("occluded")
                
                    t_polyline = t.getElementsByTagName("polyline")
                    for t_pl in t_polyline:
                        t_pl_points = t_pl.getAttribute("points")
                        t_pl_points = t_pl_points.split(";")
                        t_pl_points = np.asarray([[int(float(b)) for b in a.split(",")] for a in t_pl_points])
                        t_x = t_pl_points[:,0]
                        t_y = t_pl_points[:,1]
                        t_xy = [(x,y) for x, y in zip(t_x, t_y)]
                        if 'Reflection' in t_pl.getAttribute('label'):
                            Img = cv2.polylines(Img, np.int32([a]), 1, (255,0,0),3)
                        else:
                            Img = cv2.polylines(Img, np.int32([a]), 1, (0,0,255),3)
                    cv2.imwrite(save_folder+'/'+t_name[:15]+'mask.png', Img)
                    cv2.waitKey(0)
                    t_plg_label = t_plg.getAttribute("label")
                    t_plg_occluded = t_plg.getAttribute("occluded")
                    k += 1
