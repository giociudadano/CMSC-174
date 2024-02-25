'''
  CMSC 174 Laboratory 2: Image Filters

  File Name:    Ciudadano_lab02_hybrid.py
  Author:       Gio Ciudadano
  Modified:     23/02/2024 1:55pm
  
  Description:  This laboratory document allows the user to select two images and combine them
                together to form a hybrid image. Each step in the hybrid image process (cross-correlation,
                convolution, high pass, and low pass) may also be viewed to see the effect of different
                parameters in the preset file.
'''

import tkinter as tk
import os, ctypes, json, cv2
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk

def crossCorrelation(filePath : str, preset : dict, isDisplay : bool) -> np.array:
  '''
  Computes the cross-correlation of the given filepath with the given kernel.

  Inputs:
    filePath:   Either an RGB image (height x width x 3) or a grayscale image
                (height x width) as a numpy array.
    preset:     Contains the kernel responsible for the cross-correlation.
    isDisplay:  Whether to display the output image or not.
                
  Output:
    Return an image of the same dimensions as the input image (same width,
    height and the number of color channels)
  '''
    
  try:
    preset = preset['kernel']
  except:
    print("Cross-correlation kernel not found on preset")
    return
    
  try:
    kernelHeight, kernelWidth = np.array(preset).shape
  except:
    print("Cross-correlation kernel is empty or incorrectly formatted")
    return
    
  inputImage = cv2.imread(filePath)
  outputImage = np.empty(inputImage.shape)
    
  # Checks if the read image is grayscale or RGB. Initializes the height, width, and depth params of the image.
  if inputImage.ndim == 3:
    imageHeight, imageWidth, imageDepth = inputImage.shape
  else:
    imageHeight, imageWidth = inputImage.shape
    imageDepth = 1
    inputImage = inputImage[:, :, np.newaxis]

  # Places the image to the center of the canvas.
  canvas = np.zeros((imageHeight+kernelHeight-1, imageWidth+kernelWidth-1, imageDepth), dtype=inputImage.dtype)
  canvas[(kernelHeight//2):(imageHeight+(kernelHeight//2)), (kernelWidth//2):(imageWidth+(kernelWidth//2))] = inputImage
    
  # Samples neighbors according to the kernel and calculates the dot product to form the output image.
  for x in range(imageWidth):
    for y in range(imageHeight):
      sample = np.reshape(canvas[y:y+kernelHeight, x:x+kernelWidth], (kernelHeight * kernelWidth, imageDepth))
      outputImage[y, x] = np.dot(np.ravel(preset), sample)        

  # Checks if an output screen is to be displayed.
  if (isDisplay):
    cv2.imshow('Cross Correlation', outputImage/255)

  return outputImage

def convolution(filePath : str, preset : dict, isDisplay : bool) -> np.array:
  '''
    Computes the convolution of the given filepath with the given kernel.

    Inputs:
      filePath:   Either an RGB image (height x width x 3) or a grayscale image
                  (height x width) as a numpy array.
      preset:     Contains the kernel responsible for the cross-correlation.
      isDisplay:  Whether to display the output image or not.

    Output:
      Return an image of the same dimensions as the input image (same width,
      height and the number of color channels)
  '''

  try:
    preset['kernel']
  except:
    print("Cross-correlation kernel not found on preset")
    return

  # Simulates convolution by flipping the kernel horizontally and verically.
  # np.flip(kernel, 1) equivalent to np.fliplr
  # np.flip(kernel, 0) equivalent to np.flipud
  preset['kernel'] = np.flip(np.flip(np.array(preset['kernel']), axis=1), axis=0).tolist()
  output = crossCorrelation(filePath, preset, False)

  if (isDisplay):
    cv2.imshow('Convolution', output/255)
  return output

def gaussianBlur(sigma, height, width) -> np.array:
  '''
  Returns a Gaussian blur kernel of the given dimensions and with the given sigma.

  Input:
    sigma:  The parameter that controls the radius of the Gaussian blur.
    width:  The width of the kernel.
    height: The height of the kernel.

    Output:
      Return a kernel of dimensions width x height such that convolving it
      with an image results in a Gaussian-blurred image.
  '''
  
  # Calculates radius
  kernelX = np.arange(-((width - 1)/2), ((width + 1)/2)) ** 2
  kernelY = np.arange(-((height - 1)/2), ((height + 1)/2)) ** 2

  # Calculates Gaussian factor equal to exp(-(x^2+y^2)/(2sigma^2))/(2pi*sigma^2)
  variance = sigma * sigma
  kernelX = np.exp(- kernelX / (2 * variance))
  kernelY = np.exp(- kernelY / (2 * variance)) / (2 * variance * np.pi)

  # Computes the outer product of the two vectors and normalizes the kernel for output
  kernel = np.outer(kernelX, kernelY)
  sum = np.sum(kernelY) * np.sum(kernelX)

  return kernel / sum

def lowPass(filePath : str, preset : dict, isDisplay : bool) -> np.array:
  '''
    Computes the low pass of the given filepath with the given sigma. A low pass
    filter supresses the higher frequency components (finer details) of the image.

    Input:
    filePath:   Either an RGB image (height x width x 3) or a grayscale image
                (height x width) as a numpy array.
    preset:     Contains the blur sigma and size of the Gaussian blur.
    isDisplay:  Whether to display the output image or not.

    Output:
        Return an image of the same dimensions as the input image (same width,
        height and the number of color channels)
  '''
  try:
    preset['blur_sigma']
  except:
    print("Blur sigma not found on preset")
    return
  
  try:
    preset['blur_size']
  except:
    print("Blur size not found on preset")
    return
  
  preset['kernel'] = gaussianBlur(preset['blur_sigma'], preset['blur_size'], preset['blur_size'])
  output = convolution(filePath, preset, False)
  if (isDisplay):
    cv2.imshow('Low Pass', output/255)
  return output

def highPass(filePath : str, preset : dict, isDisplay : bool) -> np.array:
  '''
    Computes the high pass of the given filepath with the given sigma. A high pass filter
    suppresses the lower frequency components (coarse details) of the image.

    Input:
    filePath:   Either an RGB image (height x width x 3) or a grayscale image
                (height x width) as a numpy array.
    preset:     Contains the blur sigma and size of the Gaussian blur.
    isDisplay:  Whether to display the output image or not.

    Output:
      Returns an image of the same dimensions as the input image (same width,
      height and the number of color channels)
  '''
  try:
    preset['blur_sigma']
  except:
    print("Blur sigma not found on preset")
    return
  
  try:
    preset['blur_size']
  except:
    print("Blur size not found on preset")
    return

  inputImage = cv2.imread(filePath)
  output = inputImage - lowPass(filePath, preset, False)
  if (isDisplay):
    cv2.imshow('High Pass', output/255)
  return output

def createHybridImage(filePathL, filePathR, preset):
  '''
    Creates a hybrid image based on the specifications of the preset.

    Input:
    filePathL, filePathR:   Either an RGB image (height x width x 3) or a grayscale image
                            (height x width) as a numpy array.
    preset:                 Specifies the blur sigma, blur size, mixin ratio, scale factor,
                            and which image to low/high pass for the hybrid image.

    Output:
      Returns an image of the same dimensions as the input image (same width,
      height and the number of color channels)
  '''
   
  try:
    preset['image_a']['blur_sigma']
    preset['image_b']['blur_sigma']
    preset['image_a']['blur_size']
    preset['image_b']['blur_size']
    preset['image_a']['high_low']
    preset['image_b']['high_low']
    preset['mixin_ratio']
    preset['scale_factor']
  except:
    print("Missing blur sigma, blur size, high low, mixin ratio, or scale factor parameters in hybrid image")
    return

  if (preset['image_a']['high_low']).lower() == 'low':
    image_a = lowPass(filePathL, preset['image_a'], False) 
    image_b = highPass(filePathR, preset['image_b'], False)
  else:
    image_a = highPass(filePathL, preset['image_a'], False) 
    image_b = lowPass(filePathR, preset['image_b'], False)

  image_a *= 1 - preset['mixin_ratio']
  image_b *= preset['mixin_ratio']

  output = ((image_a + image_b) * preset['scale_factor']).clip(0, 255)
  cv2.imshow('Hybrid Image', output/255)
  return output

def uploadImage(widgetImageDisplay : tk.Frame, widgetFileName : tk.Label, target : str) -> None:
  '''
    Fetches an image from storage and displays the image to the widget.

    Parameters:
      widgetImageDisplay: Target widget to display image.
      widgetFileName: Target widget to display file name.
      target: Identifier if image is left or right.
  '''

  global imgL, imgR
  fileTypes = [('JPEG Image', '*.jpg'), ('PNG Image','*.png')]

  global filePathL, filePathR
  filePath = filedialog.askopenfilename(filetypes=fileTypes)
  if (filePath == None or filePath == ''):
    print("Error: No file selected")
    return
  widgetFileName['text'] = f"{os.path.basename(filePath)}"[:40]

  img = Image.open(filePath)
  width, height = img.size
  img = ImageTk.PhotoImage(img.resize((int(width * (450 / width)), int(height * (450 / height)))))
  
  if (target == 'L'):
    imgL = img
    filePathL = filePath
  elif (target == 'R'):
    imgR = img
    filePathR = filePath

  prev = tk.Button(master=widgetImageDisplay,image= img)
  prev['relief'] = 'sunken'
  prev.grid(row=0, column=0)

def uploadPreset(widgetFileName : tk.Label) -> None:

  '''
    Fetches a JSON file to be used for preset sigma and kernel weights.

    Parameters:
      widgetFileName: Target widget to display file name.
  '''

  global presetData
  fileTypes = [('JSON Files', '*.json')]
  filePath = filedialog.askopenfilename(filetypes=fileTypes)
  if (filePath == None or filePath == ''):
    print("Error: No file selected")
    return
  widgetFileName['text'] = f"{os.path.basename(filePath)}"[:40]

  file = open(filePath)
  presetData = json.load(file)

def verifyFilter(*funcs) -> None:

  def runFunctions(*args, **kwargs) -> None:

    try:
      filePathL
    except:
      print("Error: Please insert an image")
      return
    
    try:
      presetData
    except:
      print("Error: Please insert a preset")
      return
    
    for f in funcs:
      f(*args, **kwargs)

  return runFunctions


def initWindow() -> None:
  '''
    Renders the GUI for the laboratory.
  '''

  ctypes.windll.shcore.SetProcessDpiAwareness(1)
  window = tk.Tk()
  window.geometry("1200x550") 
  window.title("CMSC 174 Lab 2: Image Filters")

  # Widget Drawing
  windowFrame = tk.Frame()
  windowFrame.pack(expand=True)

  imagePreviewL = tk.Frame(master=windowFrame, background='gray85', width= 456, height = 456)
  imagePreviewL.grid(row=0, column=0, padx=10, pady=5)
  impagePreviewLText = tk.Label(master=imagePreviewL, background='gray85', text='Left Image', font=('Arial', 8))
  impagePreviewLText.place(relx=.5, rely=.5, anchor='center')
  imagePreviewLFileName = tk.Label(master=windowFrame, text='', font=('Arial', 8))
  imagePreviewLFileName.grid(row=2, column=0, padx=5, pady=2)

  imagePreviewR = tk.Frame(master=windowFrame, background='gray85', width= 456, height = 456)
  imagePreviewR.grid(row=0, column=1, padx=10, pady=5)
  impagePreviewRText = tk.Label(master=imagePreviewR, background='gray85', text='Right Image', font=('Arial', 8))
  impagePreviewRText.place(relx=.5, rely=.5, anchor='center')
  imagePreviewRFileName = tk.Label(master=windowFrame, text='', font=('Arial', 8))
  imagePreviewRFileName.grid(row=2, column=1, padx=5, pady=2)

  controls = tk.Frame(master=windowFrame)
  controls.grid(row=0, column=2, padx=10, pady=5, sticky='n')

  controlsAText = tk.Label(master=controls, text='Upload', font=('Arial', 8, 'bold'))
  controlsAText.grid(row=0, column=0, pady=5, sticky='w')
  uploadLButton = tk.Button(master=controls, text='Left Image...', width=20, font=('Arial', 8), command=lambda:uploadImage(imagePreviewL, imagePreviewLFileName, 'L'))
  uploadLButton.grid(row=1, column=0, pady=3)
  uploadRButton = tk.Button(master=controls, text='Right Image...', width=20, font=('Arial', 8), command=lambda:uploadImage(imagePreviewR, imagePreviewRFileName, 'R'))
  uploadRButton.grid(row=2, column=0, pady=3)

  filterFileName = tk.Label(master=controls, text='', fg='gray26', font=('Arial', 7))
  filterFileName.grid(row=4, column=0, padx=5, pady=2, sticky='w')
  uploadFilterPresets = tk.Button(master=controls, text='Filter Presets...', width=20, font=('Arial', 8), command=lambda:uploadPreset(filterFileName))
  uploadFilterPresets.grid(row=3, column=0, pady=3) 
 
  controlsBText = tk.Label(master=controls, text='Render', font=('Arial', 8, 'bold'))
  controlsBText.grid(row=5, column=0, pady=(20, 5), sticky='w')
  controlsBAText = tk.Label(master=controls, text='Left Image', fg='gray26', font=('Arial', 7))
  controlsBAText.grid(row=6, column=0, pady=3, sticky='w')
  crossCorrelationButton = tk.Button(master=controls, text='Cross Correlation...', width=20, font=('Arial', 8), command=verifyFilter(lambda: crossCorrelation(filePathL, presetData['single_image'], True)))
  crossCorrelationButton.grid(row=7, column=0, pady=3)
  convolutionButton = tk.Button(master=controls, text='Convolution...', width=20, font=('Arial', 8), command=verifyFilter(lambda: convolution(filePathL, presetData['single_image'], True)))
  convolutionButton.grid(row=8, column=0, pady=3)
  lowPassButton = tk.Button(master=controls, text='Low Pass...', width=20, font=('Arial', 8), command=verifyFilter(lambda: lowPass(filePathL, presetData['single_image'], True)))
  lowPassButton.grid(row=9, column=0, pady=3)
  highPassButton = tk.Button(master=controls, text='High Pass...', width=20, font=('Arial', 8), command=verifyFilter(lambda: highPass(filePathL, presetData['single_image'], True)))
  highPassButton.grid(row=10, column=0, pady=3)
  controlsBAText = tk.Label(master=controls, text='Both Images', fg='gray26', font=('Arial', 7))
  controlsBAText.grid(row=11, column=0, pady=3, sticky='w')
  hybridImageButton = tk.Button(master=controls, text='Hybrid Image...', width=20, font=('Arial', 8), command=verifyFilter(lambda: createHybridImage(filePathL, filePathR, presetData['hybrid_image'])))
  hybridImageButton.grid(row=12, column=0, pady=3)

  window.mainloop()

initWindow()