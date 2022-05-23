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


#-------------------------CLASS DOMINANT_COLORS--------------------------------#
class DOMINAN_COLORS:
    # inti function
    def __init__(self):
        
        # defining path
        self.pth = input('Enter path to the images folder: ')
        self.color_ = [('Black',(0, 0, 0)), ('Charcoal',(54, 69, 79)), ('Dark Green',(2, 48, 32)), ('Dark Purple', (48, 25, 52)),
                ('Jet Black', (52, 52, 52)), ('Licorice', (27, 18, 18)), ('Matte Black', (40, 40, 43)), ('Midnight Blue', (25, 25, 112)),
                ('Onyx', (53, 57, 53)), ('Aqua'	,(0, 255, 255)), ('Azure', (240, 255, 255)), ('Baby Blue', (137, 207, 240)),
                ('Blue', (0, 0, 255)), ('Blue Gray', (115, 147, 179)), ('Blue Green', (8, 143, 143)), ('Bright Blue', (0, 150, 255)),
                ('Cadet Blue', (95, 158, 160)), ('Cobalt Blue', (0, 71, 171)), ('Cornflower Blue', (100, 149, 237)),
                ('Cyan', (0, 255, 255)), ('Dark Blue', (0, 0, 139)), ('Denim', (111, 143, 175)), ('Egyptian Blue', (20, 52, 164)),
                ('Electric Blue', (125, 249, 255)), ('Glaucous', (96, 130, 182)), ('Jade', (0, 163, 108)), ('Indigo', (63, 0, 255)),
                ('Iris', (93, 63, 211)), ('Light Blue', (173, 216, 230)), ('Midnight Blue', (25, 25, 112)), ('Navy Blue', (0, 0, 128)),
                ('Neon Blue', (31, 81, 255)), ('Pastel Blue', (167, 199, 231)), ('Periwinkle', (204, 204, 255)), ('Powder Blue', (182, 208, 226)),
                ('Robin Egg Blue', (150, 222, 209)), ('Royal Blue', (65, 105, 225)), ('Sapphire Blue', (15, 82, 186)),
                ('Seafoam Green', (159, 226, 191)), ('Sky Blue', (135, 206, 235)), ('Steel Blue', (70, 130, 180)), ('Teal', (0, 128, 128)),
                ('Turquoise', (64, 224, 208)), ('Ultramarine', (4, 55, 242)), ('Verdigris', (64, 181, 173)), ('Zaffre', (8, 24, 168)),
                ('Almond', (234, 221, 202)), ('Brass', (225, 193, 110)), ('Bronze', (205, 127, 50)), ('Brown', (165, 42, 42)),
                ('Buff', (218, 160, 109)), ('Burgundy', (128, 0, 32)), ('Burnt Sienna', (233, 116, 81)), ('Burnt Umber', (110, 38, 14)),
                ('Camel', (193, 154, 107)), ('Chestnut', (149, 69, 53)), ('Chocolate', (123, 63, 0)), ('Cinnamon', (210, 125, 45)),
                ('Coffee', (111, 78, 55)), ('Cognac', (131, 67, 51)), ('Copper', (184, 115, 51)), ('Cordovan', (129, 65, 65)),
                ('Dark Brown', (92, 64, 51)), ('Dark Red', (139, 0, 0)), ('Dark Tan', (152, 133, 88)), ('Ecru', (194, 178, 128)),
                ('Fallow', (193, 154, 107)), ('Fawn', (229, 170, 112)), ('Garnet', (154, 42, 42)), ('Golden Brown', (150, 105, 25)),
                ('Khaki', (240, 230, 140)), ('Light Brown', (196, 164, 132)), ('Mahogany', (192, 64, 0)), ('Maroon', (128, 0, 0)),
                ('Mocha', (150, 121, 105)), ('Nude', (242, 210, 189)), ('Ochre', (204, 119, 34)), ('Olive Green', (128, 128, 0)),
                ('Oxblood', (74, 4, 4)), ('Puce', (169, 92, 104)), ('Red Brown', (165, 42, 42)), ('Red Ochre', (145, 56, 49)),
                ('Russet', (128, 70, 27)), ('Saddle Brown', (139, 69, 19)), ('Sand', (194, 178, 128)), ('Sienna', (160, 82, 45)),
                ('Tan', (210, 180, 140)), ('Taupe', (72, 60, 50)), ('Tuscan Red', (124, 48, 48)), ('Wheat', (245, 222, 179)),
                ('Wine', (114, 47, 55)), ('Ash Gray', (178, 190, 181)), ('Blue Gray', (115, 147, 179)), ('Charcoal', (54, 69, 79)),
                ('Dark Gray', (169, 169, 169)), ('Glaucous', (96, 130, 182)), ('Gray', (128, 128, 128)), ('Gunmetal Gray', (129, 133, 137)),
                ('Light Gray', (211, 211, 211)), ('Pewter', (137, 148, 153)), ('Platinum', (229, 228, 226)), ('Sage Green', (138, 154, 91)),
                ('Silver', (192, 192, 192)), ('Slate Gray', (112, 128, 144)), ('Smoke', (132, 136, 132)), ('Steel Gray', (113, 121, 126)), 
                ('Aqua', (0, 255, 255)), ('Aquamarine', (127, 255, 212)), ('Army Green', (69, 75, 27)), ('Blue Green', (8, 143, 143)),
                ('Bright Green', (170, 255, 0)),('Cadet Blue', (95, 158, 160)),('Cadmium Green', (9, 121, 105)),('Celadon', (175, 225, 175)),
                ('Chartreuse', (223, 255, 0)), ('Citrine', (228, 208, 10)), ('Cyan', (0, 255, 255)), ('Dark Green', (2, 48, 32)),
                ('Electric Blue', (125, 249, 255)), ('Emerald Green', (80, 200, 120)), ('Eucalyptus', (95, 133, 117)), ('Fern Green', (79, 121, 66)),
                ('Forest Green', (34, 139, 34)),('Grass Green', (124, 252, 0)),('Green', (0, 128, 0)),('Hunter Green', (53, 94, 59)),('Jade', (0, 163, 108)),
                ('Jungle Green', (42, 170, 138)), ('Kelly Green', (76, 187, 23)),('Light Green', (144, 238, 144)),('Lime Green', (50, 205, 50)),
                ('Lincoln Green', (71, 135, 120)), ('Malachite', (11, 218, 81)), ('Mint Green', (152, 251, 152)), ('Moss Green', (138, 154, 91)),
                ('Neon Green', (15, 255, 80)),('Nyanza', (236, 255, 220)),('Olive Green', (128, 128, 0)),('Pastel Green', (193, 225, 193)),
                ('Pear', (201, 204, 63)), ('Peridot', (180, 196, 36)), ('Pistachio', (147, 197, 114)), ('Robin Egg Blue', (150, 222, 209)),
                ('Sage Green', (138, 154, 91)), ('Sea Green', (46, 139, 87)), ('Seafoam Green', (159, 226, 191)), ('Shamrock Green', (0, 158, 96)),
                ('Spring Green', (0, 255, 127)), ('Teal', (0, 128, 128)), ('Turquoise', (64, 224, 208)), ('Vegas Gold', (196, 180, 84)),
                ('Verdigris', (64, 181, 173)), ('Viridian', (64, 130, 109)), ('Amber', (255, 191, 0)), ('Apricot', (251, 206, 177)), ('Bisque', (242, 210, 189)),
                ('Bright Orange', (255, 172, 28)),('Bronze', (205, 127, 50)),('Buff', (218, 160, 109)), ('Burnt Orange', (204, 85, 0)),
                ('Burnt Sienna', (233, 116, 81)), ('Butterscotch', (227, 150, 62)), ('Cadmium Orange', (242, 140, 40)), ('Cinnamon', (210, 125, 45)),
                ('Copper', (184, 115, 51)), ('Coral', (255, 127, 80)), ('Coral Pink', (248, 131, 121)), ('Dark Orange', (139, 64, 0)),
                ('Desert', (250, 213, 165)), ('Gamboge', (228, 155, 15)), ('Golden Yellow', (255, 192, 0)), ('Goldenrod', (218, 165, 32)),
                ('Light Orange', (255, 213, 128)), ('Mahogany', (192, 64, 0)), ('Mango', (244, 187, 68)), ('Navajo White', (255, 222, 173)),
                ('Neon Orange', (255, 95, 31)), ('Ochre', (204, 119, 34)), ('Orange', (255, 165, 0)), ('Pastel Orange', (250, 200, 152)),
                ('Peach', (255, 229, 180)), ('Persimmon', (236, 88, 0)),('Pink Orange', (248, 152, 128)),('Poppy', (227, 83, 53)),
                ('Pumpkin Orange', (255, 117, 24)), ('Red Orange', (255, 68, 51)), ('Safety Orange', (255, 95, 21)), ('Salmon', (250, 128, 114)),
                ('Seashell', (255, 245, 238)), ('Sienna', (160, 82, 45)), ('Sunset Orange', (250, 95, 85)), ('Tangerine', (240, 128, 0)),
                ('Terra Cotta', (227, 115, 94)), ('Yellow Orange', (255, 170, 51)), ('Amaranth', (159, 43, 104)), ('Bisque', (242, 210, 189)),
                ('Cerise', (222, 49, 99)), ('Claret', (129, 19, 49)), ('Coral', (255, 127, 80)), ('Coral Pink', (248, 131, 121)),
                ('Crimson', (220, 20, 60)), ('Dark Pink', (170, 51, 106)), ('Dusty Rose', (201, 169, 166)), ('Fuchsia', (255, 0, 255)),
                ('Hot Pink', (255, 105, 180)), ('Light Pink', (255, 182, 193)), ('Magenta', (255, 0, 255)), ('Millennial Pink', (243, 207, 198)),
                ('Mulberry', (119, 7, 55)), ('Neon Pink', (255, 16, 240)), ('Orchid', (218, 112, 214)), ('Pastel Pink', (248, 200, 220)),
                ('Pastel Red', (250, 160, 160)), ('Pink', (255, 192, 203)), ('Pink Orange', (248, 152, 128)), ('Plum', (103, 49, 71)),
                ('Puce', (169, 92, 104)), ('Purple', (128, 0, 128)),('Red Purple', (149, 53, 83)),('Rose', (243, 58, 106)),('Rose Gold', (224, 191, 184)),
                ('Rose Red', (194, 30, 86)), ('Ruby Red', (224, 17, 95)), ('Salmon', (250, 128, 114)), ('Seashell', (255, 245, 238)),
                ('Thistle', (216, 191, 216)), ('Watermelon Pink', (227, 115, 131)),('Amaranth', (159, 43, 104)),('Bright Purple', (191, 64, 191)),
                ('Burgundy', (128, 0, 32)), ('Byzantium', (112, 41, 99)), ('Dark Pink', (170, 51, 106)), ('Dark Purple', (48, 25, 52)),
                ('Eggplant', (72, 50, 72)), ('Iris', (93, 63, 211)), ('Lavender', (230, 230, 250)), ('Light Purple', (203, 195, 227)),
                ('Light Violet', (207, 159, 255)), ('Lilac', (170, 152, 169)), ('Mauve', (224, 176, 255)), ('Mauve Taupe', (145, 95, 109)),
                ('Mulberry', (119, 7, 55)), ('Orchid', (218, 112, 214)), ('Pastel Purple', (195, 177, 225)), ('Periwinkle', (204, 204, 255)),
                ('Plum', (103, 49, 71)), ('Puce', (169, 92, 104)), ('Purple', (128, 0, 128)), ('Quartz', (81, 65, 79)),
                ('Red Purple', (149, 53, 83)), ('Thistle', (216, 191, 216)), ('Tyrian Purple', (99, 3, 48)), ('Violet', (127, 0, 255)),
                ('Wine', (114, 47, 55)), ('Wisteria', (189, 181, 213)), ('Blood Red', (136, 8, 8)), ('Brick Red', (170, 74, 68)),
                ('Bright Red', (238, 75, 43)), ('Brown',  (165, 42, 42)),('Burgundy', (128, 0, 32)), ('Burnt Umber', (110, 38, 14)),
                ('Burnt Orange', (204, 85, 0)), ('Burnt Sienna', (233, 116, 81)), ('Byzantium', (112, 41, 99)), ('Cadmium Red', (210, 43, 43)),
                ('Cardinal Red', (196, 30, 58)), ('Carmine', (215, 0, 64)), ('Cerise', (222, 49, 99)), ('Cherry', (210, 4, 45)),
                ('Chestnut', (149, 69, 53)), ('Claret', (129, 19, 49)), ('Coral Pink', (248, 131, 121)), ('Cordovan', (129, 65, 65)),
                ('Crimson', (220, 20, 60)), ('Dark Red', (139, 0, 0)), ('Falu Red', (123, 24, 24)), ('Garnet', (154, 42, 42)),
                ('Mahogany', (192, 64, 0)), ('Maroon', (128, 0, 0)), ('Marsala', (152, 104, 104)), ('Mulberry', (119, 7, 55)),
                ('Neon Red', (255, 49, 49)),('Oxblood', (74, 4, 4)),('Pastel Red', (250, 160, 160)),('Persimmon', (236, 88, 0)),
                ('Poppy', (227, 83, 53)),('Puce', (169, 92, 104)),('Raspberry', (227, 11, 92)),('Red', (255, 0, 0)),('Red Brown', (165, 42, 42)),
                ('Red Ochre', (145, 56, 49)),('Red Orange', (255, 68, 51)),('Red Purple', (149, 53, 83)),('Rose Red', (194, 30, 86)),
                ('Ruby Red', (224, 17, 95)),('Russet', (128, 70, 27)),('Salmon', (250, 128, 114)),('Scarlet', (255, 36, 0)),
                ('Sunset Orange', (250, 95, 85)),('Terra Cotta', (227, 115, 94)),('Tuscan Red', (124, 48, 48)),('Tyrian Purple', (99, 3, 48)),
                ('Venetian Red', (164, 42, 4)),('Vermillion', (227, 66, 52)),('Wine', (114, 47, 55)),('Alabaster', (237, 234, 222)),
                ('Beige', (245, 245, 220)),('Bone White', (249, 246, 238)), ('Cornsilk', (255, 248, 220)),('Cream', (255, 253, 208)),
                ('Eggshell', (240, 234, 214)),('Ivory', (255, 255, 240)),('Linen', (233, 220, 201)),('Navajo White', (255, 222, 173)),
                ('Off White', (250, 249, 246)),('Parchment', (252, 245, 229)),('Peach', (255, 229, 180)),('Pearl', (226, 223, 210)),
                ('Seashell', (255, 245, 238)),('Vanilla', (243, 229, 171)),('White', (255, 255, 255)),('Almond', (234, 221, 202)),
                ('Amber', (255, 191, 0)),('Apricot', (251, 206, 177)),('Beige', (245, 245, 220)),('Brass', (225, 193, 110)),
                ('Bright Yellow', (255, 234, 0)),('Cadmium Yellow', (253, 218, 13)),('Canary Yellow', (255, 255, 143)),('Chartreuse', (223, 255, 0)),
                ('Citrine', (228, 208, 10)),('Cornsilk', (255, 248, 220)),('Cream', (255, 253, 208)),('Dark Yellow', (139, 128, 0)),
                ('Desert', (250, 213, 165)),('Ecru', (194, 178, 128)),('Flax', (238, 220, 130)),('Gamboge', (228, 155, 15)),('Gold', (255, 215, 0)),
                ('Golden Yellow', (255, 192, 0)),('Goldenrod', (218, 165, 32)),('Icterine', (252, 245, 95)),('Ivory', (255, 255, 240)),
                ('Jasmine', (248, 222, 126)),('Khaki', (240, 230, 140)),('Lemon Yellow', (250, 250, 51)),('Maize', (251, 236, 93)),
                ('Mango', (244, 187, 68)),('Mustard Yellow', (255, 219, 88)),('Naples Yellow', (250, 218, 94)),('Navajo White', (255, 222, 173)),
                ('Nyanza', (236, 255, 220)),('Pastel Yellow', (255, 250, 160)),('Peach', (255, 229, 180)),('Pear', (201, 204, 63)),
                ('Peridot', (180, 196, 36)),('Pistachio', (147, 197, 114)),('Saffron', (244, 196, 48)),('Vanilla', (243, 229, 171)),
                ('Vegas Gold', (196, 180, 84)),('Wheat', (245, 222, 179)),('Yellow', (255, 255, 0)),('Yellow Orange', (255, 170, 51))]
        
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
        # dominant colors array
       
    #-------------------------     CONTRAST FUNCTION   -------------------------#    
    def GET_CONTRAST_COLORS(self, pth):
        COLORS = self.DOM_COLORS(pth)
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
        for l in lst_cols_delta:
            if max(delta_) == l[2]:
                print(l)
                F_max = tuple(l[0].tolist())
                S_max = tuple(l[1].tolist())
        return F_max, S_max
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
        # append file path to LST
        LST.append(pth)
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
            # if color match to second closest color code
            if S_COL_NEAR in color:
                # appent color name to LST
                LST.append(color[0])  
        # LST.append(F_COL)
        # LST.append(S_COL)
        # return list of all reuqured data
        return LST

    #-----------------------------main FUNCTION---------------------------------#
    def main(self):
        # all the fields names in a list
        header = ["IMAGE-PATH", "IMAGE-NAME", "IMAGE-1st-DOMINANT-COLOR", "IMAGE-2nd-DOMINANT-COLOR"]
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
                # display number of images processed
                print(str(e+1), 'IMAGES PROCESSED')
                # call IMAGE_DATA function to get list of image data for each image
                lst = self.IMAGE_DATA(PTH)
                if len(lst)== 5:
                    # display data
                    del lst[-1]
                    print(lst)
                    csv_writer.writerow(lst)
                elif len(lst)== 4:
                # write one row of data for each image file
                    print(lst)
                    csv_writer.writerow(lst)
        
        return














