'''
  CMSC 174 Laboratory 2: Images

  File Name:    Ciudadano_lab02_hybrid.py
  Author:       Gio Ciudadano
  Modified:     09/02/2024 12:15am
  
  Description:  TBA
'''

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import ctypes

def uploadImage(widget : tk.Frame, target : str) -> None:
  '''
    Fetches an image from storage and displays the image to the widget.

    Parameters:
      widget: target widget to display image
      target: Identifier if image is left or right

    Returns:
      None
  '''

  global imgL, imgR
  fileTypes = [('JPEG Image', '*.jpg'), ('PNG Image','*.png')]

  filePath = filedialog.askopenfilename(filetypes=fileTypes)
  img = Image.open(filePath)
  width, height = img.size
  img = ImageTk.PhotoImage(img.resize((int(width * (400 / width)), int(height * (400 / height)))))
  
  if (target == 'L'):
    imgL = img
  else:
    imgR = img
  prev = tk.Button(master=widget,image= img)
  prev['relief'] = 'sunken'
  prev.grid(row=0, column=0)


def initWindow() -> None:
  ctypes.windll.shcore.SetProcessDpiAwareness(1)
  window = tk.Tk()
  window.geometry("1200x500") 
  window.title("CMSC 174 Lab 2: Image Filters")

  # Widget Drawing
  windowFrame = tk.Frame()
  windowFrame.pack(expand=True)
  imagePreviewL = tk.Frame(master=windowFrame, background='gray85', width= 406, height = 406)
  imagePreviewL.grid(row=0, column=0, padx=10, pady=5)
  impagePreviewLText = tk.Label(master=imagePreviewL, background='gray85', text='Left Image', font=('Arial', 8))
  impagePreviewLText.place(relx=.5, rely=.5, anchor='center')
  imagePreviewR = tk.Frame(master=windowFrame, background='gray85', width= 406, height = 406)
  imagePreviewR.grid(row=0, column=1, padx=10, pady=5)
  impagePreviewRText = tk.Label(master=imagePreviewR, background='gray85', text='Right Image', font=('Arial', 8))
  impagePreviewRText.place(relx=.5, rely=.5, anchor='center')

  controls = tk.Frame(master=windowFrame)
  controls.grid(row=0, column=2, padx=10, pady=5, sticky='n')

  controlsAText = tk.Label(master=controls, text='Upload', font=('Arial', 8, 'bold'))
  controlsAText.grid(row=0, column=0, pady=5, sticky='w')
  uploadLButton = tk.Button(master=controls, text='Left Image...', width=20, font=('Arial', 8), command=lambda:uploadImage(imagePreviewL, 'L'))
  uploadLButton.grid(row=1, column=0, pady=3)
  uploadRButton = tk.Button(master=controls, text='Right Image...', width=20, font=('Arial', 8), command=lambda:uploadImage(imagePreviewR, 'R'))
  uploadRButton.grid(row=2, column=0, pady=3)
  uploadFilterPresets = tk.Button(master=controls, text='Filter Presets...', width=20, font=('Arial', 8))
  uploadFilterPresets.grid(row=3, column=0, pady=3) 

  controlsBText = tk.Label(master=controls, text='Render', font=('Arial', 8, 'bold'))
  controlsBText.grid(row=4, column=0, pady=(20, 5), sticky='w')

  window.mainloop()

initWindow()