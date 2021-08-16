import os
import argparse
import re

import numpy as np
from skimage.metrics import structural_similarity 
from PIL import Image


def save_results(path, ssim_val, ssim_map, montage):
	'''
	Utility fucntion to save all the outputs
	'''
	os.makedirs(path, exist_ok=True)

	montage.save(os.path.join(path, 'montage.png'))
	ssim_map.save(os.path.join(path, 'ssim_map.png'))
	with open(os.path.join(path, 'ssim_val.txt'), 'w') as f:
		f.write("SSIM: " + str(ssim_val))
	

def resize_images(img1, img2, force=False):
	
	'''
	Resize the two images to match the size of the smaller one.
	If "force" is False, then it will only resize if images have same aspect ratio.
	Otherwise return None 
	'''

	w1, h1 = img1.size
	w2, h2 = img2.size

	if not force:
		ratio_orig = h1/w1
		ratio_comp = h2/w2

		if round(ratio_orig, 2) != round(ratio_comp, 2):
			return None, None, False
	
	if h1 == h2 and w1 ==w2:
		return img1, img2, True 
	elif h1 > h2:
		resized1 = img1.resize((w2, h2), Image.ANTIALIAS)
		return resized1, img2, True
	elif h2 > h1:
		resized2 = img2.resize((w1, h1), Image.ANTIALIAS)
		return img1, resized2, True


def get_ssim(img1, img2, force_resize=False):
	'''
	Inputs:
	img1: PIL image
	img2: PIL image
	force_resize: Whether to force resize the images or not, if aspect ration does not match

	Returns:
	SSIM index value bw img1 and img2, and SSIM map
	'''
	gray_img1 = img1.convert('L')
	gray_img2 = img2.convert('L')

	gray_img1, gray_img2, success = resize_images(
								gray_img1, gray_img2, force=force_resize)
	
	if success:

		gray_img1 = np.array(gray_img1)
		gray_img2 = np.array(gray_img2)


		ssim_val, ssim_map = structural_similarity(gray_img1, gray_img2, 
									full=True, gaussian_weights=True, sigma=1.5,
									data_range=gray_img2.max() - gray_img2.min())
		
		
		ssim_map = ((1 + ssim_map) /2 *255).astype(np.uint8)

		
		ssim_map = Image.fromarray(ssim_map, 'L')
		return ssim_val, ssim_map
	else:
		return None, None


def get_montage(images):
	'''
	Inputs:
	images: A list of images
	
	Returns:
	Montage of all the images in the list concatenated horizontally
	'''

	widths, heights = zip(*(i.size for i in images))
	total_width = sum(widths)
	max_height = max(heights)

	montage = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
		montage.paste(im, (x_offset,0))
		x_offset += im.size[0]
	
	return montage


def main(args):

	subdirs = [(f.path, f.name) for f in os.scandir(args.root_dir) if f.is_dir()]
	if not len(subdirs) > 0:
		print("There are not sub-dirs at the given path {}".format(args.root_dir))
		exit()
	else:
		print("{} sub-directories found. Running SSIM...".format(len(subdirs)))
	
	exts = '.*.(' + '|'.join(args.img_types) + ')'
	os.makedirs(args.save_dir, exist_ok=True)

	for path, name in subdirs:
		image_paths = [img for img in os.listdir(path) if re.match(exts, img, re.IGNORECASE)][:2] #take first 2 images for ssim
		images = [Image.open(os.path.join(path, x)) for x in image_paths]

		montage = get_montage(images)
		ssim_val, ssim_map = get_ssim(images[0], images[1], args.force_resize)

		if ssim_val is not None and ssim_map is not None:
			save_results(os.path.join(args.save_dir, name), ssim_val, ssim_map, montage)
			print("Images Subidr: {}, SSIM: {}".format(name, ssim_val))
		else:
			print("Aspect ratio does not match for images at path \"{}\". Use --force argumnet to calcualte ssim anyways". format(name))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='SSIM Generator')

	parser.add_argument("--root-dir", default='data', type=str,
						help="Path for root directory containing all the sub-dirs. Default: ./data")
	parser.add_argument("--save-dir", default='output', type=str,
						help="Path where montage and ssim maps are saved")
	parser.add_argument('--img-types', default=['png', 'jpg'], nargs='+',
							help="List of extensions for images. Default: ['png', 'jpg']",
							choices=['jpg','jpeg','png','tiff','bmp','gif'])
	parser.add_argument('--force-resize', '--force_resize', action='store_true',
						help='Use this argument to calcualte SSIM for image pairs whose aspect ratios do not match.'\
							'By default, the program ignores such pairs.')
	
	args = parser.parse_args()

	main(args)