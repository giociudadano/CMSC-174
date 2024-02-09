'''
  CMSC 174 Laboratory 1: Image Splitter

  File Name:    Ciudadano_lab1.py
  Author:       Gio Ciudadano
  Modified:     09/02/2024 12:15am
  
  Description:  This program allows the user to split an image into four identical images. The
                user may define the number of rows and columns on the output image.
'''

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import os, cv2, ctypes
import numpy as np


def initWindow() -> None:
  # Creates a window that allows the user to select a file.
  # The currently selected file is displayed for which the splitted image can be rendered.
  
  def uploadFile() -> None:
    # Opens the file explorer and prompts the user to select a file.
    # Displays the selected file in the window.
    global img
    fileTypes = [('JPEG Image', '*.jpg'), ('PNG Image','*.png')]

    global filePath
    filePath = filedialog.askopenfilename(filetypes=fileTypes)
    if filePath == '':
      labelInfo['text'] = "No image selected"
      return
    else:
      labelInfo['text'] = f"Image successfully selected"

    img = Image.open(filePath)
    labelTitle.pack_propagate(True) 

    # Destroys previously uploaded image
    for child in imagePreview.winfo_children():
      child.destroy()

    # Resizes uploaded image
    width, height = img.size
    if (height >= width):
      img = ImageTk.PhotoImage(img.resize((int(width * (350 / height)), 350)))
    else:
      img = ImageTk.PhotoImage(img.resize((550, min(int(height * (550 / width)), 350))))

    prev = tk.Button(master=imagePreview,image=img)
    prev['relief'] = 'sunken'
    prev.grid(row=0, column=0)
    buttonRenderImage['state'] = 'normal'

  def renderImage() -> None:
    # Renders the image.
    try:
      rows : int = int(rowsTextbox.get('1.0','end-1c'))
      columns : int = int(columnsTextbox.get('1.0','end-1c'))
    except:
      labelInfo['text'] = 'Please enter an integer'
      return
    
    image = cv2.imread(filePath)
    height, width, _ = image.shape
    image = np.rot90(np.vstack([image[np.mod(np.arange(height), int((height/rows) * 2)) < int(height/rows)], image[np.mod(np.arange(height), int((height/rows) * 2)) >= int(height/rows)]]))
    image = np.rot90(np.vstack([image[np.mod(np.arange(width), int((width/columns) * 2)) < int(width/columns)], image[np.mod(np.arange(width), int((width/columns) * 2)) >= int(width/columns)]]), k=3)
    
    success = cv2.imwrite(os.getcwd() + "/" + "out" + "/" + os.path.basename(filePath), image)
    if success:
      labelInfo['text'] = f"Image saved at out/{os.path.basename(filePath)}"[:40]
    else:
      labelInfo['text'] = "Failed to save image"

    cv2.imshow('Rendered Image', image)
    cv2.waitKey()
    cv2.destroyAllWindows()

  ctypes.windll.shcore.SetProcessDpiAwareness(1)
  window = tk.Tk()
  window.geometry("600x500") 
  window.title("CMSC 174 Lab 1: Image Splitter")

  windowFrame = tk.Frame()
  windowFrame.pack(expand=True)
  labelTitle = tk.Label(master=windowFrame, text='Image Splitter', font=('Arial', 12, 'bold'))
  labelTitle.grid(row=0, column=0, pady=5)
  imagePreview = tk.Frame(master=windowFrame, background='gray85', width= 350, height = 350)
  imagePreview.grid(row=1, column=0, pady=5)
  imagePreview.pack_propagate(False) 
  labelImagePreview = tk.Label(master=imagePreview, background='gray85', text='Image Preview', font=('Arial', 8))
  labelImagePreview.place(relx=.5, rely=.5, anchor='center')
  controls = tk.Frame(master=windowFrame)
  controls.grid(row=2, column=0, pady=5)
  buttonUploadFile = tk.Button(master=controls, text='Select a File', width=12, font=('Arial', 8), command=lambda:uploadFile())
  buttonUploadFile.grid(row=0, column=0, padx=5)
  rowsLabel = tk.Label(master=controls, text='Rows', font=('Arial', 8))
  rowsLabel.grid(row=0, column=2, padx=(30, 5))
  rowsTextbox = tk.Text(master=controls, height=1, width= 5)
  rowsTextbox.grid(row=0, column=3, padx=5)
  columnsLabel = tk.Label(master=controls, text='Columns', font=('Arial', 8))
  columnsLabel.grid(row=0, column=4, padx=5)
  columnsTextbox = tk.Text(master=controls, height=1, width= 5)
  columnsTextbox.grid(row=0, column=5, padx=5)
  buttonRenderImage = tk.Button(master=controls, text='Render Image', width=12, font=('Arial', 8), state='disabled', command=lambda:renderImage())
  buttonRenderImage.grid(row=1, column=2, padx=5, pady=2, columnspan=4, sticky='e')
  labelInfo = tk.Label(master=controls, text='', font=('Arial', 8))
  labelInfo.grid(row=1, column=0, padx=5, pady=2, columnspan=4, sticky='w')

  window.mainloop()

os.system('cls')
initWindow()