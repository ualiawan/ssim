# SSIM calculator

This program takes a directory containing sub-directories with image pairs, and computes SSIM between respective pairs. The program logs as well as saves the results.

## Requirements:
1. Pyhton > =3.6
2. Numpy
3. Scikit-image
4. PIL

## How to run:
to execute this program, you can execute following command from terminal:

```
python run.py --root-dir $PATH_TO_ROOT_DIRECTORY --save-dir $PATH_TO_SAVE_DIRECTORY
```

Exmaple:
```
python run.py --root-dir data --save-dir output
```

### Arguments

1. --roor-dir (default: data): Path to root directory containing all the sub-folders with image pairs.
2. --save-dir (default: output): Path where to save the output images and results
3. --img-types (default: ['png', 'jpg']): A lsit of image types (extensions) to look for in each sub-direcotry. You can choose any number of values from ['jpg','jpeg','png','tiff','bmp','gif']
4. --force-resize (default: False): SBy default, the program ignores the image pairs who does not have matching aspect ratios, as resizing such images will distort the images. Set this argument if you want to force resize all images irrespective of their aspect ratio.

## Directory Structure:
The program expects follwing directory structure in the path specified by --root-dir argument:

```
root
|___ subdir1
|     |___ imagex.png
|     |___ imagey.png
|___ subdir2
|     |___ imagex.png
|     |___ imagey.png
|___ ...
```

## Outputs:

Output directory structure is something like this:
```
output
|___ subdir1
|     |___ montage.png
|     |___ ssim_map.png
|     |___ ssim_val.txt
|___ subdir2
|     |___ montage.png
|     |___ ssim_map.png
|     |___ ssim_val.txt
|___ ...
```

### Notes on SSIM Values and Maps:

1. SSIM value in scikit-image is supposed to have the same results as in the original Matlab implementation by Wang et al in "Image quality assessment: From error visibility to structural similarity". 
These values are slightly **different** from the built-in Matlab implementation of SSIM

2. Scikit-image has a range of [-1, 1] for pixel level SSIM. Hence the results have some negative values as well in the SSIM map. In order to save the SSIM map, I have normalized the range between [0, 1] by doing (1 + SSIM) / 2. I am not sure how Matlab internally handles it, if you have better ideas, I would be happy to implement. 
