import tkinter as tk
import os
from tkinter import ttk
from tkinter.filedialog import askopenfilename

MIROPRESS_EXTENSION = 'mir'


def compressClicked():
    global status_var
    global MIROPRESS_EXTENSION
    global fileName
    global statusLabel
    if not fileName:
        status_var.set('Invalid Input')
        statusLabel.config(fg='red')
        return
    compressedFileName = fileName[:fileName.rfind('.')+1] + MIROPRESS_EXTENSION
    print("compress")
    try:
        print(fileName)
        os.system('python3 LZcompress.py ' + fileName + ' ' + compressedFileName)
        status_var.set('Compressed Succesfully')
        statusLabel.config(fg='green')
    except:
        print("something went wrong")
        status_var.set('Something went wrong')
        statusLabel.config(fg='red')
    
def extractClicked():
    global status_var
    global MIROPRESS_EXTENSION
    global fileName
    global statusLabel
    global extName
    decompressedExt = extName.get()
    if not fileName or not decompressedExt:
        status_var.set('Invalid Input')
        statusLabel.config(fg='red')
        return
    decompressedFileName = fileName[:fileName.rfind('.')+1] + decompressedExt
    try:
        os.system('python3 LZdecompress.py ' + fileName + ' ' + decompressedFileName)
        status_var.set('Extracted Succesfully')
        statusLabel.config(fg='green')
    except:
        print("something went wrong")
        status_var.set('Something went wrong')
        statusLabel.config(fg='red')
    


def chooseClicked():
    global MIROPRESS_EXTENSION
    global fileName
    global input_var
    fileName = askopenfilename()
    labelText = fileName[fileName[:fileName.rfind('/')].rfind('/'):]
    input_var.set(labelText)

fileName = ''

master = tk.Tk()

window_width = '400'
window_height = '150'
master.title('MiroPress')
master.geometry(window_width+'x'+window_height)

# Compress Button
compressButton = tk.Button(master, text="Compress File", command = compressClicked, width=12, fg='blue')
compressButton.place(y = 48, x = 30)

# Extract Button
extractButton = tk.Button(master, text="Extract File", command = extractClicked, width=12, fg='green')
extractButton.place(y = 84, x = 30)

# Decompressed File Extension
extName = tk.Entry(master, width = 15)
extName.place(y = 120, x = 30)


# Choose Button
chooseFileButton = tk.Button(master, text="Choose", command = chooseClicked, width=18)
chooseFileButton.place(y = 113, x = int(window_width)/2 - 20)

# Label for Input File Name
input_var = tk.StringVar(master)
input_var.set("No File Chosen")
inputFileNameLabel = tk.Label(master, textvariable=input_var)
inputFileNameLabel.place(y = 50, x = int(window_width)/2 - 20)

# Label for Output File Name
output_var = tk.StringVar(master)
output_var.set("as")
outputFileNameLabel = tk.Label(master, textvariable=output_var)
outputFileNameLabel.place(y = 80, x = int(window_width)/2 - 20)

# Label for Compress Status
status_var = tk.StringVar(master)
status_var.set("")
statusLabel = tk.Label(master, textvariable=status_var)
statusLabel.place(y = 3, x = int(window_width)/2 - 15)

# ProgressBar
mpb = ttk.Progressbar(master, orient ="horizontal",length = 350, mode ="determinate")
mpb.place(y = 24, x = 25)
mpb["maximum"] = 100
mpb["value"] = 5

tk.mainloop()
