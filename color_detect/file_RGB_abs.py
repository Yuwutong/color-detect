import math
import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import math
import os
import pandas as pd


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
		
read_folder = file_path+'/Ruo'
save_folder = file_path+'/Ruo_abs'
mkdir(save_folder)

save_txt = save_folder + '/RGB_txt.txt'
f = open(save_txt,'a', encoding="utf-8")
f.write('*******RG  GB  BR\n')
f.close()
  
for path,d,filelist in g:  
    for filename in filelist:
        if filename.endswith('png'):
            pic_file=read_folder + '/' + filename
            # pic_file=os.path.join(file_path+'/'+filename)
            # print(pic_file)
            (picture_file, tempfilename) = os.path.split(os.path.join(file_path, filename))
            (file_name, extension) = os.path.splitext(tempfilename)
            # picture = file_path + '/' + file_name + extension

            img_bgr = cv2.imread(pic_file, cv2.IMREAD_COLOR)
            img_b = img_bgr[..., 0]
            img_g = img_bgr[..., 1]
            img_r = img_bgr[..., 2]

            [rows, cols] = img_r.shape
            img_RG = np.mat(np.zeros((rows,cols)))
            img_GB = np.mat(np.zeros((rows,cols)))
            img_BR = np.mat(np.zeros((rows,cols)))

            for i in range(rows):
                for j in range(cols):
                    img_RG[i,j] = math.fabs(int(img_r[i,j]) - int(img_g[i,j]))
                    img_GB[i,j] = math.fabs(int(img_g[i,j]) - int(img_b[i,j]))
                    img_BR[i,j] = math.fabs(int(img_b[i,j]) - int(img_r[i,j]))
                    
                   
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
            final_save_folder_RG = save_folder + '/' + file_name +'_RG.png'
            plt.savefig(final_save_folder_RG)
            plt.show();
            Pover20_RG = len([1 for i in array_RG if i > 20])/len([1 for i in array_RG if i > 0])
            #print(file_name,'_RG','percent: {:.2%}'.format(Pover20, '.00%'))
            f.write(file_name+'   ')
            f.write(format(round(Pover20_RG,2), '.00%')+'   ')
            
            
            G_B_hist = plt.hist(array_GB, bins=80, facecolor="green", edgecolor="green")
            plt.xlabel("G-B_value")
            plt.ylabel("number of pixel")
            plt.xlim([1,60])
            plt.title("G_B")
            final_save_folder_GB = save_folder + '/' + file_name +'_GB.png'
            plt.savefig(final_save_folder_GB)
            plt.show()
            Pover20_GB = len([1 for i in array_RG if i > 20])/len([1 for i in array_RG if i > 0])
            #print(file_name,'_RG','percent: {:.2%}'.format(Pover20, '.00%'))
            f.write(format(round(Pover20_GB,2), '.00%')+'   ')
    

            B_R_hist = plt.hist(array_BR, bins=80, facecolor="blue", edgecolor="blue")
            plt.xlabel("B_R_value")
            plt.ylabel("number of pixel")
            plt.xlim([1,60])
            plt.title("B_R")
            final_save_folder_BR = save_folder + '/' + file_name +'_BR.png'
            plt.savefig(final_save_folder_BR)
            plt.show()
            Pover20_BR = len([1 for i in array_RG if i > 20])/len([1 for i in array_RG if i > 0])
            #print(file_name,'_RG','percent: {:.2%}'.format(Pover20, '.00%'))
            f.write(format(round(Pover20_BR,2), '.00%'))
            
            
            f.write('\n')
            f.close()
            
    
            



