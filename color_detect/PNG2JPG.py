# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 22:31:05 2020

@author: mastaffs
"""

import os

path="D:/css/HSVtest1J"
file_walk = os.walk(path)
fileNum = 0
filesPathList = []
for root, dirs, files in file_walk:
    # print(root, end=',')
    # print(dirs, end=',')
    # print(files)
    for file in files:
        fileNum = fileNum + 1
        filePath = root + '/' + file
        # print(filePath)
        filesPathList.append(filePath)
        protion = os.path.splitext(filePath)
        # print(protion[0],protion[1])

        if protion[1].lower() == '.png':
            print("doing：" + filePath)
            newFilePath = protion[0] + '.JPG'
            os.rename(filePath, newFilePath)