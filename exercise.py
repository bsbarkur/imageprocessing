from matplotlib import pyplot as plt

import Image
import ImageDraw
import numpy as np
import cv2
import pytesseract
import os
import sys
import shutil

# Load an color image in grayscale
#img = cv2.imread('Creatives/VW_728x90.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('Creatives/320x480[3].jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('Creatives/Gionee_320x480.jpg', cv2.IMREAD_COLOR)


def get_colors(infile, outfile, numcolors=10, swatchsize=20, resize=150):
	image = Image.open(infile)
	image = image.resize((resize, resize))
	result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
	result.putalpha(0)
	colors = result.getcolors(resize*resize)

	print len(sorted(colors))

	pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
	draw = ImageDraw.Draw(pal)

    	posx = 0
    	for count, col in colors:
       	 	draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
        	posx = posx + swatchsize
 	
    	del draw
    	pal.save(outfile, "PNG") 

def processImage(infiles, cur_list, dest):
	for infile in infiles:
		ofilename = infile.split(".")[0]
   		try:
        		im = Image.open('Creatives/'+infile)
    		except IOError:
        		print "Cant load", infile
        		sys.exit(1)
    		i = 0
    		mypalette = im.getpalette()

    		try:
        		while 1:
            			im.putpalette(mypalette)
            			new_im = Image.new("RGB", im.size)
            			new_im.paste(im)
		
            			new_im.save(ofilename + '.jpg')
				pfile = ofilename + '.jpg'
            			i += 1
            			im.seek(im.tell() + 1)
				if (os.path.isfile(dest+'Creatives/'+pfile)) == False:
					shutil.move(dest + pfile, dest+'Creatives/')
					cur_list.append(pfile)
    		except EOFError:
        		pass # end of sequence
 	return cur_list

def readDirectoryOfImages(path):
	curated_files_list = []
	curated_gif_files_list = []
	list_files = os.listdir(path)
	for f in list_files:
		if (f == '.DS_Store'):
			continue
		elif (f == 'Intel_Dynamic_GIF Banner.gif' or f == 'CISCOGEN041I01_WO-13_Mosaic-Banner_Blender_300x250.gif' or f == '320-x-250.gif' or f == 'airline_travel_insurance-728X90.gif' or f == 'airline_travel_insurance300x250.gif'):
			curated_gif_files_list.append(f)
		else:
			curated_files_list.append(f) 
	return curated_gif_files_list, curated_files_list

def call_image_operations(flist):
	print flist
	for f in flist:
		print f
		call_image_load(f)

def call_image_load(file):
	img_file = 'Creatives/' + file
	print img_file
	#img = cv2.imread(img_file, cv2.IMREAD_COLOR)
	img = cv2.imread(img_file)

	print len(img)
	shape_tuple = img.shape
	print shape_tuple
	row_position = shape_tuple[0]/2
	col_position = shape_tuple[1]/2
	print img[row_position][col_position]


def call_average(file):
	img = Image.open(file)
	pixels = img.load() # this is not a list, nor is it list()'able
	width, height = img.size

	all_pixels = []
	for x in range(width):
		for y in range(height):
			cpixel = pixels[x, y]
			all_pixels.append(cpixel)
	
	r = 0
	g = 0
	b = 0
	counter = 0
	for pixel in all_pixels:
		r = r + pixel[0]
		g = g + pixel[1]
		b = b + pixel[2]
		counter = counter + 1	
	
	print r/counter, g/counter, b/counter
	
def call_gradient(file):
	img = cv2.imread(file, cv2.IMREAD_COLOR)

	laplacian = cv2.Laplacian(img,cv2.CV_64F)
	sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
	sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

	plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
	plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
	plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
	plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

	plt.show()

def call_text_miner(file):
	print pytesseract.image_to_string(Image.open(file))

if __name__ == "__main__":
	curated_list = []
	total_list = []
	path = '/Users/bsb/Code/AdNear/Creatives/'
	bpath = '/Users/bsb/Code/AdNear/'
	gif_file_list , file_list = readDirectoryOfImages(path)
	curated_list = file_list
	print "--- created non gif file list -----"
	print curated_list
	print "-- processing gifs in the directory ---"
	total_list = processImage(gif_file_list, curated_list, bpath)
	print total_list
	print "-- calling image operations on the file list ---"
	call_image_operations(total_list)
	#call_gradient('airline_travel_insurance300x250.png')
	#call_average('airline_travel_insurance300x250.png')
	call_text_miner('Creatives/VW_728x90.jpg')
    	#get_colors('airline_travel_insurance300x250.png', 'outfile.png')
