import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import time
import LZcompress
import LZdecompress

MIROPRESS_EXTENSION = 'mir'


def removeThings():
    global fileName
    global input_var
    global output_var
    input_var.set('No File Chosen')
    output_var.set('')
    fileName = ''


def compressClicked():
    global status_var
    global time_var
    global MIROPRESS_EXTENSION
    global fileName
    global statusLabel
    if not fileName:
        status_var.set('Invalid Input')
        statusLabel.config(fg='red')
        removeThings()
        return
    compressedFileName = fileName[:fileName.rfind('.')+1] + MIROPRESS_EXTENSION
    print('compressedFileName:', compressedFileName)
    try:
        startTime = time.time()
        LZcompress.main(fileName, compressedFileName)
        time_var.set(str(time.time()-startTime))
        status_var.set('Compressed Succesfully')
        statusLabel.config(fg='green')
        output_var.set(
            compressedFileName[compressedFileName[:compressedFileName.rfind('/')].rfind('/'):])
    except:
        print('oh shit')
        status_var.set('Something went wrong')
        statusLabel.config(fg='red')
        removeThings()


def extractClicked():
    global status_var
    global output_var
    global MIROPRESS_EXTENSION
    global fileName
    global statusLabel
    global extName
    decompressedExt = extName.get()
    if not fileName or not decompressedExt:
        status_var.set('Invalid Input')
        statusLabel.config(fg='red')
        removeThings()
        return
    decompressedFileName = fileName[:fileName.rfind('.')+1] + decompressedExt
    try:
        startTime = time.time()
        LZdecompress.main(fileName, decompressedFileName)
        time_var.set(str(time.time()-startTime))
        status_var.set('Extracted Succesfully')
        statusLabel.config(fg='green')
        output_var.set(
            decompressedFileName[decompressedFileName[:decompressedFileName.rfind('/')].rfind('/'):])
    except:
        status_var.set('Something went wrong')
        statusLabel.config(fg='red')
        removeThings()


def chooseClicked():
    global MIROPRESS_EXTENSION
    global fileName
    global input_var
    fileName = askopenfilename()
    if fileName:
        status_var.set('')
    print('fileName:', fileName)
    labelText = fileName[fileName[:fileName.rfind('/')].rfind('/'):]
    print('labelText:', labelText)
    input_var.set(labelText)


fileName = ''

master = tk.Tk()

window_width = '400'
window_height = '150'
master.title('MiroPress')
master.geometry(window_width+'x'+window_height)

# Compress Button
compressButton = tk.Button(
    master, text="Compress File", command=compressClicked, width=12, fg='blue')
compressButton.place(y=48, x=30)

# Extract Button
extractButton = tk.Button(master, text="Extract File",
                          command=extractClicked, width=12, fg='green')
extractButton.place(y=84, x=30)

# Decompressed File Extension
extName = tk.Entry(master, width=15)
extName.place(y=120, x=30)


# Choose Button
chooseFileButton = tk.Button(
    master, text="Choose", command=chooseClicked, width=18)
chooseFileButton.place(y=113, x=int(window_width)/2 - 20)

# Label for Input File Name
input_var = tk.StringVar(master)
input_var.set("No File Chosen")
inputFileNameLabel = tk.Label(master, textvariable=input_var)
inputFileNameLabel.place(y=50, x=int(window_width)/2 - 20)

# Label for Output File Name
output_var = tk.StringVar(master)
output_var.set("")
outputFileNameLabel = tk.Label(master, textvariable=output_var)
outputFileNameLabel.place(y=80, x=int(window_width)/2 - 20)

# Label for Compress Status
status_var = tk.StringVar(master)
status_var.set("")
statusLabel = tk.Label(master, textvariable=status_var)
statusLabel.place(y=12, x=int(window_width)/2, anchor=tk.CENTER)


# Label for Status Text
statusText_var = tk.StringVar(master)
statusText_var.set("Status:")
statusTestLabel = tk.Label(master, textvariable=statusText_var)
statusTestLabel.place(y=12, x=54, anchor=tk.CENTER)


# Label for Time
time_var = tk.StringVar(master)
time_var.set("")
timeLabel = tk.Label(master, textvariable=time_var)
timeLabel.place(y=32, x=int(window_width)/2, anchor=tk.CENTER)

# Label for Time text
timeText_var = tk.StringVar(master)
timeText_var.set("Time:")
timeTextLabel = tk.Label(master, textvariable=timeText_var)
timeTextLabel.place(y=32, x=50, anchor=tk.CENTER)


tk.mainloop()
