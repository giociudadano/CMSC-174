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
  '''
    Creates and returns a gaussian and laplacian stack of a given image.
      Gaussian stack: Applies a Gaussian filter to the current image and pushes it to the stack.
      Laplacian stack: Calculates the difference between the current image and the last image in the stack.
    
    Parameters:
      image - The current image to create a stack with. Requires np.array type.
  '''
  gaussian_stack = [image]
  laplacian_stack = []
  for i in range(0, STACK_SIZE):
    gaussian_stack.append(scipy.ndimage.gaussian_filter(gaussian_stack[i].astype(np.float32), sigma=16))
    laplacian_stack.append(gaussian_stack[i]-gaussian_stack[i+1])
  return gaussian_stack, laplacian_stack

def create_blended_image(image_a : np.array, image_b : np.array, mask: np.array):
  '''
    Seamlessly creates a blended image by combining the Laplacian stacks of the given images for each layer.
    Weights and filters the given images using a Gaussian stack of the given image mask.

    Parameters:
      image_a, image_b - The images to seamlessly blend.
      mask - Defines the weights to blend the image.
  '''
  _, laplacian_a = create_gaussian_laplacian_stack(image_a)
  _, laplacian_b = create_gaussian_laplacian_stack(image_b)
  gaussian_mask, _ = create_gaussian_laplacian_stack(mask)
  
  blend = []
  for i in range(STACK_SIZE):
    blend.append((laplacian_a[i] * (gaussian_mask[i+1]/255)) + (laplacian_b[i] * (1-(gaussian_mask[i+1]/255))))
  blended_image = cv2.normalize(sum(blend), None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
  cv2.imwrite('Ciudadano_lab03_blendvert.png', blended_image*255)
  cv2.imshow('Blended Image', blended_image)
  cv2.waitKey(0)
  
'''
  Prompts the user to select an image display option.
'''
selectedOption : str = display_laboratory_details()
match selectedOption:
  case "1":
    try:
      image_a = cv2.imread("Ciudadano_lab03_left.png")
      image_b = cv2.imread("Ciudadano_lab03_right.png")
      mask = cv2.imread("Ciudadano_lab03_verticalmask.png")
    except:
      raise Exception("Could not find images or image mask")
    create_blended_image(image_a, image_b, mask)
  case "2":
    try:
      image_a = cv2.imread("Ciudadano_lab03_crazyone.png")
      image_b = cv2.imread("Ciudadano_lab03_crazytwo.png")
      mask = cv2.imread("Ciudadano_lab03_crazymask.png")
    except:
      raise Exception("Could not find images or image mask")
    create_blended_image(image_a, image_b, mask)
  case _:
    raise Exception("No option selected. Please run the program again.")