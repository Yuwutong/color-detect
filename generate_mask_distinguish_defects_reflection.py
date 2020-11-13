# Read 20200205 VS1 VS2 (20p).xml
# Generate masks accordingly
import xml.dom.minidom
import numpy as np
from PIL import Image 
from PIL import ImageDraw
import os


src_folder = 'D:/video/New folder'
save_folder = 'd:/chow_extra/wait_for_name'
os.makedirs(save_folder,exist_ok=True)

folders = os.listdir(src_folder)
for folder in folders:
    print(folder)
    subfolders = os.listdir(os.path.join(src_folder,folder))
    for subfolder in subfolders:
        print(subfolder)
        dom = xml.dom.minidom.parse(os.path.join(src_folder,folder,subfolder, subfolder+'.xml'))
        root = dom.documentElement

        images = root.getElementsByTagName('image')

        i=0
        t = images[i] #'10360575526(G)-R1-Darkfield-01-1.png'
        t_name = t.getAttribute("name")
        
        for t in images:
        	t_name = t.getAttribute("name")
        	t_width = t.getAttribute("width")
        	t_height = t.getAttribute("height")
        
        	img = Image.open(os.path.join(src_folder,folder,subfolder,t_name))
        	img.save(os.path.join(save_folder,t_name))
        
        	# t_img = img
        	t_img = Image.new('RGB', (int(t_width), int(t_height)))
        	draw = ImageDraw.Draw(t_img)
        
        	t_polygon = t.getElementsByTagName("polygon")
        	for t_plg in t_polygon:
        		t_plg_points = t_plg.getAttribute("points")
        		t_plg_points = t_plg_points.split(";")
        		t_plg_points = np.asarray([[int(float(b)) for b in a.split(",")] for a in t_plg_points])
        		t_x = t_plg_points[:,0]
        		t_y = t_plg_points[:,1]
        		t_xy = [(x,y) for x,y in zip(t_x,t_y)]
        		if 'Reflection' in t_plg.getAttribute("label"):
        			draw.polygon(t_xy,fill='red')
        		else:
        			draw.polygon(t_xy,fill='blue')
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
        			draw.polygon(t_xy, fill='red')
        		else:
        			draw.polygon(t_xy, fill='blue')
        		t_pl_label = t_pl.getAttribute("label")
        		t_pl_occluded = t_pl.getAttribute("occluded")
        
        	t_img.save(os.path.join(save_folder, t_name[:11]+'_mask.png'))
        	print(i,t_name[:11] + ' saved ...')
        	i=i+1
        
