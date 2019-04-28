# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:02:48 2018

@author: wyses
"""

# LICENSING
#This code is licensed according to the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
#International License.

#------------------------------------------------------------------------------

import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from skimage import measure
import os

#Check if the desired output file exists (here we used "PINradSeedSizeResults.txt"),
#if it doesn't, create it, if it does, open it to append results to it

if 'PINradSeedSizeResults.txt' not in os.listdir():
    outfile = open('PINradSeedSizeResults.txt', 'w')
    outfile.write('SeedID' + "\t" + 'Area_mm2' + "\t" + 'Length_mm' + "\t" + 'Width_mm' + "\t" + 'Perimeter_mm' + "\n")
    outfile.close()

outfile = open('PINradSeedSizeResults.txt', 'a')

#Cone ID numbers (obtained from image names), will go through all images in the
#specified folder, here we put our images with scanned seeds in the folder "Radiata seeds images_toRun"
#one image per cone, containing all 10 seeds measured.  Arranged in order down the page, seed number 1 - 10
ConeIDs = os.listdir(os.path.join(os.getcwd(),'Radiata seeds images_toRun'))

for cone in ConeIDs:
    ConeID = cone.split('.')[0]
    
    img = plt.imread(os.path.join('Radiata seeds images_toRun', ConeID+'.jpg'))
    img = img.astype('int16')
    img = img[70:(img.shape[0]-70), 70:(img.shape[1]-70), 1]
        

        
    seed = img < 245
    
       
    # label connected regions that satisfy this condition
    labels, nlabels = ndimage.label(seed)
        
    fig = plt.figure()
    ax = fig.add_subplot(111)    
    ax.imshow(np.ma.masked_array(labels, ~seed), cmap=plt.cm.gist_rainbow) 
    ax.set_title('Imaged seeds')
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
    
    #account for noise by assuming that largest objects are the seeds, 
    #but ignoring the label scanned into the image with cone ID info
    
    #Resolution (in dpi) and pixels per mm
    res = 600
    px_mm2 = (res**2)/645.16
    px_mm = res/25.4
    
    areas = np.bincount(labels.ravel())[1:]
    label_seed = np.where((areas > 16*px_mm2) * (areas < 1500*px_mm2) == True)[0]


    #calculate area of the seeds in pixels
    area = np.bincount(labels.ravel())[1:][label_seed]
    
    #calculate perimeter, length, and width of the seed in pixels
    
    properties = measure.regionprops(labels)
    perimeter = np.array([prop.perimeter for prop in properties])[label_seed]
    length= np.array([prop.major_axis_length for prop in properties])[label_seed]
    width= np.array([prop.minor_axis_length for prop in properties])[label_seed]
    
    
    #convert px measurements to mm   
    area_mm2 = area/px_mm2
    length_mm = length/np.sqrt(px_mm2)
    width_mm = width/np.sqrt(px_mm2)
    perimeter_mm = perimeter/np.sqrt(px_mm2)
    
    print(len(label_seed))
    
    for n in range(len(label_seed)):
        #write out the values
        area = str(round(area_mm2[n], 2))
        length = str(round(length_mm[n], 2))
        width = str(round(width_mm[n], 2))
        perimeter = str(round(perimeter_mm[n], 2))
        SeedID = ConeID+str(n+1)
        
        outfile.write(SeedID + "\t" + area + "\t" + length + "\t" + width + "\t" + perimeter + "\n")

outfile.close()
