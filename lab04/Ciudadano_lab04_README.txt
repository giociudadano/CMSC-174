CMSC 174 Laboratory 4: Fluid Volume Estimation
Gio Carlo Ciudadano

ABOUT
In this laboratory course, we were tasked to estimate the volume of a given fluid inside a container using Computer Vision, Image Filtering, and Thresholding. Thresholding in image filtering is the process of zero-ing out pixels that are below or above a certain specified value, and this can then be used through image processing to further isolate objects from a given image such as fluids from a container. From the isolated set of shapes formed from thresholding, the volume of the fluid can then be measured by calculating the area of the shapes.

This laboratory document makes use of Image Filtering and Thresholding by first converting the target image to grayscale or single channel and then using Thresholding to identify a matrix of edges in the image. The edges were then smoothed out multiple times using cv2.dilate() and cv2.erode() to smooth-out the edges being formed. We then constructed a set of contours from the given images using cv2.findContours() and then measured the area for each contour using cv2.contourArea(). After finding the area of each contour, the contour with the largest area above and below certain pre-determined values was selected as the fluid area. The selected area was then divided by a constant value pre-selected from calibrating the images with known volumes.

In this laboratory document, the user is tasked to select from seven different directories, four of which have known volumes and three of which have not. For each given directory, the volume for each image inside the directory is calculated and the average of all the images in the selected directory is displayed as the volume of the fluid inside the container.

RESULTS
The program determined the following values from the directories with unknown volumes (with calibration constant = 850 pixels^2/mL):
data/A/ - 118.23 mL
data/B/ - 197.06 mL
data/C/ - 346.48 mL

DIRECTORY
data - Contains the images for this laboratory.
Ciudadano_lab04.py - Contains the source code for this laboratory.
Ciudadano_lab04_README.txt - Contains this text file.