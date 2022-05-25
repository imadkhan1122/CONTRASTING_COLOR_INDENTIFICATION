#------------------------import important packages-----------------------------#
import cv2
import glob
import os
from sklearn.cluster import KMeans
from math import sqrt
import csv
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import pandas as pd
from PIL import ImageColor

df = pd.read_excel('colors.xlsx', index_col=False)
primary_names = []
colors_ = []
for i, j,  in df.iterrows():
    RGB_ = ImageColor.getcolor(j[0], "RGB")
    colors_.append(tuple((j[1], RGB_)))
    primary_names.append(tuple((j[1], j[2])))

COLORS = colors_
PRIMARY_NAMES = primary_names
#-------------------------CLASS DOMINANT_COLORS--------------------------------#
class DOMINAN_COLORS:
    # inti function
    def __init__(self):
        
        # defining path
        self.pth = input('Enter path to the images folder: ')
        self.color_ = COLORS
        self.primaryColors = PRIMARY_NAMES
                
        # call main function
        self.main()
    #-----------------------LOADING IMAGES FUNCTION-----------------------------#
    def LOAD_IMGS(self, pth):
        # list of images possible formats
        ext = ['png', 'jpg', 'jpeg']    # Add image formats here
        # empty list variable
        files = []
        # append images path to files list
        [files.extend(glob.glob(pth + '/' + '*.' + e)) for e in ext]
        # return list of images paths
        return files
    #-----------------------DOM COLORS EXTRACTOR--------------------------------#
    def DOM_COLORS(self, pth):
        # extractting totol of 5 colors
        clusters = 10 # try changing it
        # loading image file using opencv
        #read image
        img = cv2.imread(pth)
        
        #convert to rgb from bgr
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
        #reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        
        #using k-means to cluster pixels
        kmeans = KMeans(n_clusters = clusters)
        kmeans.fit(img)
        COLORS = kmeans.cluster_centers_
        #the cluster centers are our dominant colors.
        return COLORS
       
    #-------------------------     CONTRAST FUNCTION   -------------------------#    
    def GET_CONTRAST_COLORS(self, pth):
        COLORS = self.DOM_COLORS(pth)
        COLORS = COLORS.tolist()
        lst_cols_delta = []
        delta_ = []
        
        F_max = ''
        S_max = ''
        for this in COLORS:
            for that in COLORS:
                # Red Color
                color1_rgb = sRGBColor(this[0], this[1], this[2]);
                
                # Blue Color
                color2_rgb = sRGBColor(that[0], that[1], that[2]);
                # Convert from RGB to Lab Color Space
                color1_lab = convert_color(color1_rgb, LabColor);

                # Convert from RGB to Lab Color Space
                color2_lab = convert_color(color2_rgb, LabColor);

                # Find the color difference
                delta_e = delta_e_cie2000(color1_lab, color2_lab);
                lst_cols_delta.append(tuple((this, that, delta_e)))
                delta_.append(delta_e)
        lst = []
        for l in lst_cols_delta:
            if max(delta_) == l[2]:
                for e, i in enumerate(COLORS):
                    if i == l[0]:
                        lst.append([e,tuple(i)])
                    if i == l[1]:
                        lst.append([e, tuple(i)])
        
        if lst[0][0] < lst[1][0]:
            F_max = lst[0][1]
        else:
            F_max = lst[1][1]
        if lst[0][0] > lst[1][0]:
            S_max = lst[0][1]
        else:
            S_max = lst[1][1]

        F_max = [round(i) for i in F_max]
        S_max = [round(i) for i in S_max]
        return tuple(F_max), tuple(S_max)
    #-----------------------TO CLOSEST COLOR IN COLORS LIST---------------------#
    def closest_color(self, rgb, colors):
        # defining three colors code
        r, g, b = rgb      
        # empty list for color codes saving
        color_diffs = []
        # itterate over colors list
        for color in colors:
            # saving three colors codes in variavle for each color
            cr, cg, cb = color
            # finding nearest color code in colors with given color code
            color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
            # append colors defference into empty list
            color_diffs.append((color_diff, color))
        # return nearest color in list
        return min(color_diffs)[1]
    #-----------------------EXTRACT IMAGE_DATA---------------------------------#
    def IMAGE_DATA(self, pth):
        # define empty list
        PRIM_NAMES = self.primaryColors
        LST = []  
        # define temprary empty list
        temp_lst = []
        # empty list to store unques colors names and its codes
        lst = []
        # itterate over colors list
        for c in set(self.color_):
            # append unique tuples of colors
            lst.append(c)
            # append unique colors codes 
            temp_lst.append(c[1])
        # convert temp_list to tuple
        COLORS = tuple(temp_lst)
        # split path to extract file name
        img_name = os.path.split(pth)[1]
        # append file name to LST
        LST.append(img_name)
        # calling DOM_COLORS function to get first and second dominant color
        F_COL, S_COL= self.GET_CONTRAST_COLORS(pth)
        
        # print(F_COL, S_COL)
        # call closest_color function to get first closest color in color list
        F_COL_NEAR = self.closest_color(F_COL, COLORS)
        # call closest_color function to get second closest color in color list
        S_COL_NEAR = self.closest_color(S_COL, COLORS)
        # itterate over colors list
        for color in lst:
            # if color match with 1st color
            if F_COL_NEAR in color:
                # append 1st color name to LST
                LST.append(color[0])
                for prim in PRIM_NAMES:
                    if color[0] in prim:
                        LST.append(prim[1])
            # if color match to second closest color code
            if S_COL_NEAR in color:
                # appent color name to LST
                LST.append(color[0])  
                for prim in PRIM_NAMES:
                    if color[0] in prim:
                        LST.append(prim[1])
        # LST.append(F_COL)
        # LST.append(S_COL)
        # return list of all reuqured data
        return LST

    #-----------------------------main FUNCTION---------------------------------#
    def main(self):
        # all the fields names in a list
        header = ["Image-Name", "First-Dominant-Color", "First-Dominant-Color-Primary", "Second-Dominant-Color", "Second-Dominant-Primary"]
        # call load_imgs function to get list of images paths in path variable
        path = self.LOAD_IMGS(self.pth)
        # create and open output.csv file
        with open('Output.csv', 'w', newline = '') as output_csv:
            # initialize rows writer
            csv_writer = csv.writer(output_csv)
            # write headers to the file
            csv_writer.writerow(header)
            # itterate over images paths
            for e, PTH in enumerate(path):      
                # call IMAGE_DATA function to get list of image data for each image
                lst = self.IMAGE_DATA(PTH)
                if len(lst)== 5:
                    # display data
                    print(lst)
                    csv_writer.writerow(lst)
                # display number of images processed
                print(str(e+1), 'IMAGES PROCESSED')
        
        return














