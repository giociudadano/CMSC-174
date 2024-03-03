'''
  CMSC 174 Laboratory 3: Image Blending

  File Name:    Ciudadano_lab03_blending.py
  Author:       Gio Ciudadano
  Modified:     02/03/2024 9:28pm
  
  Description:  This program makes use of Laplacian and Gaussian stacks to creatively
                blend two images together.
'''

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import scipy

STACK_SIZE = 5

def display_laboratory_details() -> str:
  '''
    Displays information about the current laboratory and prompts the user to select an option.
  '''

  os.system('cls')
  print("\x1b[38;5;129mWelcome to CMSC 174 Laboratory 3: Image Blending")
  print("\x1b[38;5;177mThis program makes use of Laplacian and Gaussian stacks to creatively\nblend two images together.\n")
  print("\x1b[38;5;228mSELECT OPTION\x1b[37m")
  print("1. Show Vertically-Blended Image")
  print("2. Show Creatively-Blended Image")
  return input("\n\x1b[38;5;228mPlease select an option:\x1b[37m ")

def create_gaussian_laplacian_stack(image: np.array):
  gaussian_stack = [image]
  laplacian_stack = []
  for i in range(1, STACK_SIZE+1):
    gaussian_stack.append(scipy.ndimage.gaussian_filter(gaussian_stack[i-1].astype(np.float32), sigma=16, radius=40))
    laplacian_stack.append(gaussian_stack[i-1]-gaussian_stack[i])
  return gaussian_stack, laplacian_stack

def create_blended_image(image_a : np.array, image_b : np.array, mask: np.array):
  _, laplacian_a = create_gaussian_laplacian_stack(image_a)
  _, laplacian_b = create_gaussian_laplacian_stack(image_b)
  gaussian_mask, _ = create_gaussian_laplacian_stack(mask)
  
  blend = []
  for i in range(STACK_SIZE):
    blend.append((laplacian_a[i] * (gaussian_mask[i+1]/255)) + (laplacian_b[i] * (1-(gaussian_mask[i+1]/255))))
  blended_image = sum(blend)
  plt.imshow(blended_image, cmap='gray')
  plt.show()

selectedOption : str = display_laboratory_details()
match selectedOption:
  case "1":
    try:
      image_a = cv2.imread("Ciudadano_lab03_left.png", cv2.IMREAD_GRAYSCALE)
      image_b = cv2.imread("Ciudadano_lab03_right.png", cv2.IMREAD_GRAYSCALE)
      mask = cv2.imread("Ciudadano_lab03_verticalmask.png", cv2.IMREAD_GRAYSCALE)
    except:
      raise Exception("Could not find 'Ciudadano_lab03_left.png', 'Ciudadano_lab03_right.png', or 'Ciudadano_lab03_verticalmask.png'")
    create_blended_image(image_a, image_b, mask)
  case _:
    raise Exception("No option selected. Please run the program again.")