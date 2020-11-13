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
                for RG_boundary in [10,13,16,19,21,24]:
                    for GB_boundary in [13,16,19,21,24,27]:
                        for BR_boundary in [13,16,19,21,24,27]:
                            for boundary_point in [15,25,35,45,55,75]:
                                R = 0
                                T = 0
                                R_true = 0
                                T_true = 0
                                for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]:
                                    t = images[i]
                                    t_name = t.getAttribute("name")
                                
                                    img_file_path = xml_path + '/' +  t_name
                                    img = Image.open(img_file_path)
                                    Img = cv2.imread(img_file_path)
                                
                                
                                    file_path = 'D:/a_RGB_291_350_abs'      
                                    save_folder = file_path+'/'+ file[-3:] + '%d'%i	
                                    read_folder = save_folder
                                    g = os.walk(read_folder)
                                    save_abs_folder = save_folder+'_abs'
                                    
                                    # save_txt = file_path + '/RGB_test.txt'
                                    # f = open(save_txt,'w', encoding="utf-8")
                                    # f.write('**********RG      GB      BR      sum\n')
                                    # f.close()
                                  
                                    for path,d,filelist in g:  
                                        for filename in filelist:
                                            if 'dst' in filename:#if filename.endswith('png')&&filename.startwith():
                                                pic_file=read_folder + '/' + filename
                                                (picture_file, tempfilename) = os.path.split(os.path.join(file_path, filename))
                                                (file_name, extension) = os.path.splitext(tempfilename)
                                                # print(pic_file)
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
                                            
                                                    # f = open(save_txt,'a', encoding="utf-8")
                                                    p = 0
                                
                                                    # Pover20_RG = len([1 for p in array_RG if p > 18])/len([1 for p in array_RG if p > 0])
                                                    array_RG = array_RG - RG_boundary
                                                    array_RG[array_RG < 0] = 0
                                                    array_RG = np.power(array_RG, 1)
                                                    # f.write(file_name+'   ')
                                                    # f.write(format(round(Pover20_RG,2), '.00%')+'   ')
                                                    # f.write(str(np.sum(array_RG))+'   ')
                                            
                                            
                                                    # Pover20_GB = len([1 for p in array_GB if p > 18])/len([1 for p in array_GB if p > 0])
                                                    array_GB = array_GB - GB_boundary
                                                    array_GB[array_GB < 0] = 0
                                                    array_GB = np.power(array_GB, 1)
                                                    # f.write(format(round(Pover20_GB,2), '.00%')+'   ')
                                                    # f.write(str(np.sum(array_GB))+'   ')
                                    
                                    
                                                    # Pover20_BR = len([1 for p in array_BR if p > 23])/len([1 for p in array_BR if p > 0])
                                                    array_BR = array_BR - BR_boundary
                                                    array_BR[array_BR < 0] = 0
                                                    array_BR = np.power(array_BR, 1)
                                                    #print(file_name,'_RG','percent: {:.2%}'.format(Pover20, '.00%'))
                                                    # f.write(format(round(Pover20_BR,2), '.00%'))
                                                    # f.write(str(np.sum(array_BR))+'   ')
                                                    # f.write(str(np.sum(array_RG)+np.sum(array_GB)+np.sum(array_BR))+'  ')
                                            
                                                    # f.write('\n')
                                                    # f.close()                                                    
                                 
                                                    if 're' in pic_file:
                                                        R = R + 1
                                                        if np.sum(array_RG)+np.sum(array_GB)+np.sum(array_BR) > boundary_point:
                                                            R_true = R_true + 1
                                                    
                                                    else:
                                                        T = T + 1
                                                        if np.sum(array_RG)+np.sum(array_GB)+np.sum(array_BR) <= boundary_point:
                                                            T_true = T_true + 1
                                    
                                                if not os.path.exists(pic_file):
                                                    break     
                                                
                                
                                if R_true/R+T_true/T > 1.3:
                                        print(RG_boundary,end = " ")
                                        print(GB_boundary,end = " ")
                                        print(BR_boundary,end = " ")
                                        print(boundary_point,end = " ")
                                        print(R_true/R+T_true/T,end = "   ")
                                        print(R_true/R,end = " ")
                                        print(T_true/T,end = " ") 
                                        R_wrong = (T - T_true)/(R_true + T - T_true) 
                                        T_wrong = (R - R_true)/(T_true + R - R_true)
                                        print((T - T_true)/(R_true + T - T_true),end = " ")
                                        print((R - R_true)/(T_true + R - R_true))
                                        # f = open(save_txt,'a', encoding="utf-8")
                                        # f.write(str(np.sum(array_RG)+np.sum(array_GB)+np.sum(array_BR))+'  ')


