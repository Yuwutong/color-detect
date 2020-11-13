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
                
                    file_path = 'D:/a_RGB_291_350_abs'
                
                    def mkdir(path):
                 
                        folder = os.path.exists(path)
                 
                        if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
                            os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
                            print("--- new folder...  ---")
                            print("---  OK  ---")
                        else:
                            print("---  There is this folder!  ---")
                        
                    save_folder = file_path+'/'+ file[-3:] + '%d'%i
                    mkdir(save_folder)
                
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
                        if 'Reflection' in t_plg.getAttribute("label"):
                            cv2.imwrite(save_folder + '/redst_%d.png'%(k), dst)
                        else:
                            cv2.imwrite(save_folder + '/dst_%d.png'%(k), dst)
                
                        cv2.waitKey(0)
                        t_plg_label = t_plg.getAttribute("label")
                        t_plg_occluded = t_plg.getAttribute("occluded")
                        k += 1
                        
                	
                    read_folder = save_folder
                    g = os.walk(read_folder)
                    save_abs_folder = save_folder+'_abs'
                    mkdir(save_abs_folder)
                
                    save_txt = save_abs_folder + '/RGB_txt.txt'
                    f = open(save_txt,'w', encoding="utf-8")
                    f.write('*******RG  GB  BR\n')
                    f.close()
                  
                    for path,d,filelist in g:  
                        for filename in filelist:
                            if filename.endswith('png'):
                                pic_file=read_folder + '/' + filename
                                (picture_file, tempfilename) = os.path.split(os.path.join(file_path, filename))
                                (file_name, extension) = os.path.splitext(tempfilename)
                                print(pic_file)
                                if os.path.exists(pic_file):
                                    img_bgr = cv2.imread(pic_file, cv2.IMREAD_COLOR)
                                    img_b = img_bgr[..., 0]
                                    img_g = img_bgr[..., 1]
                                    img_r = img_bgr[..., 2]
                
                                    [rows, cols] = img_r.shape
                                    img_RG = np.mat(np.zeros((rows,cols)))
                                    img_GB = np.mat(np.zeros((rows,cols)))
                                    img_BR = np.mat(np.zeros((rows,cols)))
                
                                    for a in range(rows):
                                        for b in range(cols):
                                            img_RG[a,b] = math.fabs(int(img_r[a,b]) - int(img_g[a,b]))
                                            img_GB[a,b] = math.fabs(int(img_g[a,b]) - int(img_b[a,b]))
                                            img_BR[a,b] = math.fabs(int(img_b[a,b]) - int(img_r[a,b]))
                                       
                                    arrayRG=np.array(img_RG)
                                    arrayGB=np.array(img_GB)
                                    arrayBR=np.array(img_BR)
                                    array_RG=arrayRG.flatten()
                                    array_GB=arrayGB.flatten()
                                    array_BR=arrayBR.flatten()
                            
                                    f = open(save_txt,'a', encoding="utf-8")
                
                                    R_G_hist = plt.hist(array_RG, bins=90, facecolor="red", edgecolor="red")
                                    plt.xlabel("R-G_value")
                                    plt.ylabel("number of pixel")
                                    plt.xlim([1,60])
                                    plt.title("R-G")
                                    final_save_folder_RG = save_abs_folder + '/' + file_name +'_RG.jpg'
                                    plt.savefig(final_save_folder_RG)
                                    plt.show();
                                    Pover20_RG = len([1 for p in array_RG if p > 20])/len([1 for p in array_RG if p > 0])
                                    f.write(file_name+'   ')
                                    f.write(format(round(Pover20_RG,2), '.00%')+'   ')
                            
                            
                                    G_B_hist = plt.hist(array_GB, bins=80, facecolor="green", edgecolor="green")
                                    plt.xlabel("G-B_value")
                                    plt.ylabel("number of pixel")
                                    plt.xlim([1,60])
                                    plt.title("G_B")
                                    final_save_folder_GB = save_abs_folder + '/' + file_name +'_GB.jpg'
                                    plt.savefig(final_save_folder_GB)
                                    plt.show()
                                    Pover20_GB = len([1 for p in array_GB if p > 20])/len([1 for p in array_GB if p > 0])
                                    f.write(format(round(Pover20_GB,2), '.00%')+'   ')
                    
                
                                    B_R_hist = plt.hist(array_BR, bins=80, facecolor="blue", edgecolor="blue")
                                    plt.xlabel("B_R_value")
                                    plt.ylabel("number of pixel")
                                    plt.xlim([1,60])
                                    plt.title("B_R")
                                    final_save_folder_BR = save_abs_folder + '/' + file_name +'_BR.jpg'
                                    plt.savefig(final_save_folder_BR)
                                    plt.show()
                                    Pover20_BR = len([1 for p in array_BR if p > 20])/len([1 for p in array_BR if p > 0])
                                    #print(file_name,'_RG','percent: {:.2%}'.format(Pover20, '.00%'))
                                    f.write(format(round(Pover20_BR,2), '.00%'))
                            
                                    f.write('\n')
                                    f.close()
                                if not os.path.exists(pic_file):
                                    break
             
                
                
                
                
                
                
                