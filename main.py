from Tkinter import Tk
import tkFileDialog
from tkFileDialog import askopenfilename
import cv2
import numpy as np

#Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
#filenames = tkFileDialog.askopenfilenames(filetypes = (("jpeg files","*.jpg"),("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
filenames = ['img1.jpg', 'img2.jpg', 'img3.jpg']


if len(filenames) < 1:
    exit()

images = [cv2.imread(x) for x in filenames]
images_grayscale = [cv2.cvtColor(x, cv2.COLOR_BGR2GRAY) for x in images]

# Find size of image1

sz = images_grayscale[0].shape

for idx in range(1,len(images_grayscale)):
    warp_mode = cv2.MOTION_AFFINE
    warp_matrix = np.eye(2, 3, dtype=np.float32)

    # Specify the number of iterations.
    number_of_iterations = 100;
    
    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-10;
    
    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
    
    # Run the ECC algorithm. The results are stored in warp_matrix.
    (cc, warp_matrix) = cv2.findTransformECC(images_grayscale[0], 
        images_grayscale[idx],warp_matrix, warp_mode, criteria)
    
    images[idx] = cv2.warpAffine(images[idx], warp_matrix, (sz[1],sz[0]), 
        flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);


images = np.stack(images, axis=3)
print images.shape

images = np.median(images, axis=3).astype(images.dtype)

print images.shape

# cv2.namedWindow('img1', cv2.WINDOW_NORMAL)
#cv2.resizeWindow("img1", 600, 600)
cv2.imshow("s9ad", images)
cv2.waitKey(0)

'''
# Read the images to be aligned
im1 =  cv2.imread("img1.jpg");
im2 =  cv2.imread("img2.jpg");
 
# Convert images to grayscale
im1_gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
im2_gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
 
# Find size of image1
sz = im1.shape
 
# Define the motion model
warp_mode = cv2.MOTION_AFFINE
#warp_mode = cv2.MOTION_EUCLIDEAN
#warp_mode = cv2.MOTION_TRANSLATION
# Define 2x3 or 3x3 matrices and initialize the matrix to identity
if warp_mode == cv2.MOTION_HOMOGRAPHY :
    warp_matrix = np.eye(3, 3, dtype=np.float32)
else :
    warp_matrix = np.eye(2, 3, dtype=np.float32)
 
# Specify the number of iterations.
number_of_iterations = 100;
 
# Specify the threshold of the increment
# in the correlation coefficient between two iterations
termination_eps = 1e-10;
 
# Define termination criteria
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
 
# Run the ECC algorithm. The results are stored in warp_matrix.
(cc, warp_matrix) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix, warp_mode, criteria)
 
if warp_mode == cv2.MOTION_HOMOGRAPHY :
    # Use warpPerspective for Homography 
    im2_aligned = cv2.warpPerspective (im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
else :
    # Use warpAffine for Translation, Euclidean and Affine
    im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);

cv2.namedWindow('img1', cv2.WINDOW_NORMAL)
cv2.namedWindow('img2', cv2.WINDOW_NORMAL)
cv2.namedWindow('img2A', cv2.WINDOW_NORMAL) 
cv2.namedWindow('and', cv2.WINDOW_NORMAL)
 
cv2.resizeWindow("img1", 600, 600)
cv2.resizeWindow("img2", 600, 600)
cv2.resizeWindow("img2A", 600, 600)
cv2.resizeWindow('and', 600, 600)

# Show final results
cv2.imshow("img1", im1)
cv2.imshow("img2", im2)
cv2.imshow("img2A", im2_aligned)
cv2.imshow("and", cv2.bitwise_and(im1, im2_aligned))

cv2.waitKey(0)
'''
