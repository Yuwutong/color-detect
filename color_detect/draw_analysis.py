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
xml_file = 'D:/data/20200408  (351 - 410)/20200324 CityU VVS2 to SI2 (D)/20200324 CityU VVS2 to SI2 (D).xml'###

dom = xml.dom.minidom.parse(xml_file)
root = dom.documentElement
images = root.getElementsByTagName('image')
e = math.e
# i = 3
#[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]:
    t = images[i]
    t_name = t.getAttribute("name")

    img_file_path = 'D:/data/20200408  (351 - 410)/20200324 CityU VVS2 to SI2 (D)/'+t_name###
    img = Image.open(img_file_path)
    Img = cv2.imread(img_file_path)

    t_polygon = t.getElementsByTagName("polygon")
    k = 1

    file_path = 'D:/a_RGB_351_410_abs'

    def mkdir(path):
 
        folder = os.path.exists(path)
 
        if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
            print("--- new folder...  ---")
            print("---  OK  ---")
        else:
            print("---  There is this folder!  ---")
        
    save_folder = file_path+'/RuoD'+'%d'%i###
        
	
    read_folder = save_folder
    g = os.walk(read_folder)
    save_abs_folder = save_folder+'_subtraction_e'
    mkdir(save_abs_folder)

    save_txt = save_abs_folder + '/RGB_20_20_20_txt.txt'
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
                            img_RG[a,b] = int(e**(0.06*(math.fabs(int(img_r[a,b]) - int(img_g[a,b])))))
                            img_GB[a,b] = int(e**(0.06*(math.fabs(int(img_g[a,b]) - int(img_b[a,b])))))
                            img_BR[a,b] = int(e**(0.06*(math.fabs(int(img_b[a,b]) - int(img_r[a,b])))))
                       
                    arrayRG=np.array(img_RG)
                    arrayGB=np.array(img_GB)
                    arrayBR=np.array(img_BR)
                    array_RG=arrayRG.flatten()
                    array_GB=arrayGB.flatten()
                    array_BR=arrayBR.flatten()
            
                    f = open(save_txt,'a', encoding="utf-8")

                    R_G_hist = plt.hist(array_RG, bins=80, facecolor="red", edgecolor="red")
                    plt.xlabel("R-G_value")
                    plt.ylabel("number of pixel")
                    plt.xlim([1,40])
                    plt.title("R-G")
                    final_save_folder_RG = save_abs_folder + '/' + file_name +'_RG.jpg'
                    plt.savefig(final_save_folder_RG)
                    plt.show();
                    Pover20_RG = len([1 for p in array_RG if p > 20])/len([1 for p in array_RG if p > -255])
                    f.write(file_name+'   ')
                    f.write(format(round(Pover20_RG,2), '.00%')+'   ')
            
            
                    G_B_hist = plt.hist(array_GB, bins=80, facecolor="green", edgecolor="green")
                    plt.xlabel("G-B_value")
                    plt.ylabel("number of pixel")
                    plt.xlim([1,40])
                    plt.title("G_B")
                    final_save_folder_GB = save_abs_folder + '/' + file_name +'_GB.jpg'
                    plt.savefig(final_save_folder_GB)
                    plt.show()
                    Pover20_GB = len([1 for p in array_GB if p > 20])/len([1 for p in array_GB if p > -255])
                    f.write(format(round(Pover20_GB,2), '.00%')+'   ')
    

                    B_R_hist = plt.hist(array_BR, bins=80, facecolor="blue", edgecolor="blue")
                    plt.xlabel("B_R_value")
                    plt.ylabel("number of pixel")
                    plt.xlim([1,40])
                    plt.title("B_R")
                    final_save_folder_BR = save_abs_folder + '/' + file_name +'_BR.jpg'
                    plt.savefig(final_save_folder_BR)
                    plt.show()
                    Pover20_BR = len([1 for p in array_BR if p > 20])/len([1 for p in array_BR if p > -255])
                    #print(file_name,'_RG','percent: {:.2%}'.format(Pover20, '.00%'))
                    f.write(format(round(Pover20_BR,2), '.00%'))
            
                    f.write('\n')
                    f.close()
                if not os.path.exists(pic_file):
                    break