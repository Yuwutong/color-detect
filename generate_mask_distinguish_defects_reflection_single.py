# Read 20200205 VS1 VS2 (20p).xml
# Generate masks accordingly
import xml.dom.minidom
import numpy as np
from PIL import Image 
from PIL import ImageDraw
import os
import pygame

save_folder = 'D:/data/471-530_D135'
xml_file = 'D:/data/20200327  (291 - 350)/20200310 CityU VVS2 SI1 SI2 (D)/20200310 CityU VVS2 SI1 SI2 (D).xml'


dom = xml.dom.minidom.parse(xml_file)
root = dom.documentElement

images = root.getElementsByTagName('image')

i = 7
t = images[i]  #'10360575526(G)-R1-Darkfield-01-1.png'

t_name = t.getAttribute("name")
t_width = t.getAttribute("width")
t_height = t.getAttribute("height")

# img = Image.open('D:/data/471-530_D135/10373793761(G)-R1-Darkfield-01.png')
img_file_path = 'D:/data/20200327  (291 - 350)/20200310 CityU VVS2 SI1 SI2 (D)/'+t_name
#t_img = img
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
  pygame.draw.lines(t_xy, fill='red')
 else:
  draw.polygon(t_xy,fill='blue')
 t_plg_label = t_plg.getAttribute("label")
 t_plg_occluded = t_plg.getAttribute("occluded")
 t_img.save(os.path.join(save_folder,t_name[:15]+'_mask.png'))

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

t_img.save(os.path.join(save_folder,t_name[:15]+'_mask.png'))
print(i,t_name[:15] + ' saved ...')
i=i+1
