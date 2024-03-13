'''
  CMSC 174 Laboratory 4: Fluid Volume Estimation

  File Name:    Ciudadano_lab04.py
  Author:       Gio Ciudadano
  Modified:     02/03/2024 9:28pm
  
  Description:  This program makes use of image filtering and thresholding to
                estimate the volume of a fluid inside a container.
'''

import os
import numpy as np
import cv2

# Calibration constants. Adjusted when changing collections.
CALIBRATION_MINIMUM_THRESHOLD = 83        # Defines the threshold cutoff and number of dilate/erode iterations when finding edges for contour construction.
CALIBRATION_DILATE_ERODE_ITERS = 5

CALIBRATION_PIXEL_VALUE = 850             # Defines the value of a pixel in the contour area. Lower number means higher pixel value.
CALIBRATION_MINIMUM_AREA_SIZE = 1000      # Defines the minimum and maximum sizes for contour rejection when finding the container with the fluid.
CALIBRATION_MAXIMUM_AREA_SIZE = 400000

def display_laboratory_details() -> str:
  '''
    Displays information about the current laboratory and prompts the user to select an option.
  '''

  os.system('cls')
  print("\x1b[38;5;129mWelcome to CMSC 174 Laboratory 4: Volume Estimation")
  print("\x1b[38;5;177mThis program makes use of image filtering and thresholding\nto estimate the volume of a fluid inside a container.\n")
  print("\x1b[38;5;228mSELECT IMAGE\x1b[37m")
  print("1. 50mL\t\t5. Unknown A")
  print("2. 100mL\t6. Unknown B")
  print("3. 200mL\t7. Unknown C")
  print("4. 350mL")
  return input("\n\x1b[38;5;228mPlease select an option:\x1b[37m ")

def get_volume(image : np.array):
  '''
    Uses thresholding to isolate possible fluids and construct a set of contours. Selects a contour containing the fluid based on criteria.
    Measures the area of the selected contour and calculates the volume using a pre-defined calibration constant.

    Parameters:
      Image - The image for which a container contains an unspecified volume of a fluid.

    Returns:
      Volume - The volume of a fluid in a container from the given image.

  '''
  
  # Converts the image to grayscale and uses thresholding to find edges, then dilates and erodes multiple times to further isolate the edges.
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  _, edges = cv2.threshold(image_gray, CALIBRATION_MINIMUM_THRESHOLD,255,cv2.THRESH_BINARY)
  edges = cv2.dilate(edges, None, iterations=CALIBRATION_DILATE_ERODE_ITERS)
  edges = cv2.erode(edges, None, iterations=CALIBRATION_DILATE_ERODE_ITERS)
  
  # From the given edges, constructs a list of contours. Checks the area of each contour and rejects contours that are too small or too large based
  # on pre-defined calibration constants.
  contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
  contours_filtered = []
  contours_filtered_area = []
  for contour in contours:
    contour_area = cv2.contourArea(contour)
    if (contour_area > CALIBRATION_MINIMUM_AREA_SIZE and contour_area < CALIBRATION_MAXIMUM_AREA_SIZE):
      contours_filtered.append(contour)
      contours_filtered_area.append(contour_area)

  # Selects the largest of the accepted contours as the contour containing the fluid inside a container and divides it with a pre-defined calibration
  # constant to get the total volume of the fluid. 
  return max(contours_filtered_area)/CALIBRATION_PIXEL_VALUE

def get_average_volume(dir):
  '''
    Finds and prints the average volume of all images in a directory.

    Parameters:
      Dir - Directory of the containing images.
  '''


  total_volume : float = 0
  files = os.listdir(os.fsencode(dir))
  print("")

  # Loops through each image file and runs get_volume() to get the volume of a fluid inside a container from each image.
  for file in files:
    file_path = f"{dir}/{file.decode('ascii')}"
    image = cv2.imread(file_path)
    volume = get_volume(image)
    print(f"Reading image at {file_path}...\t{volume:.2f} mL")
    total_volume += volume

  print(f"\nThe total fluid in the container is about \x1b[38;5;154m{total_volume/len(files):.2f}\x1b[37m mL\n")

selectedOption : str = display_laboratory_details()
match selectedOption:
  case "1": dir = "data/50mL"
  case "2": dir = "data/100mL"
  case "3": dir = "data/200mL"
  case "4": dir = "data/350mL"
  case "5": dir = "data/guess/A"
  case "6": dir = "data/guess/B"
  case "7": dir = "data/guess/C"
  case _: raise Exception("No option selected. Please run the program again.")
get_average_volume(dir)
