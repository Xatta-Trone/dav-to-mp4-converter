import glob
import subprocess
import threading
from tkinter import *
from tkinter import filedialog, messagebox
from ffmpeg_progress_yield import FfmpegProgress
import os


def scanFiles():
    if folder_path.get() == "" : 
        messagebox.showerror(title="Error!!",message="Please select a folder first.")
    files.clear()
    for filename in glob.iglob(folder_path.get() + '**/**', recursive=True):
        
        if filename.endswith('.dav'):
            files.insert(0,filename)
        # print(filename)
    totalFiles.set(f"Total files: {len(files)}")
    totalComplete.set(f"{completedFiles}/{len(files)} files converted")
    print(files)

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askdirectory()

    if len(filename) > 0 :
        folder_path.set(filename)
        folder_string.set(folder_path.get())
    else:
        folder_string.set("Please select a folder")
    print("filename")
    print(filename)
    print("filename")

def folder_to_save_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askdirectory()

    if len(filename) > 0 :
        output_folder_path.set(filename)
        output_folder_string.set(output_folder_path.get())
    else:
        folder_string.set("Please select a folder to save")
    print("filename")
    print(filename)
    print("filename")
def convertFiles():
    if(check_ffmpeg() == False): 
        messagebox.showerror(title="Error!!",message="Please install ffmpeg first")
    elif(output_folder_path.get() == ""):
        messagebox.showerror(title="Error!!",message="Please select a folder to save.")
    else:    
        for idx,file in enumerate(files):
            convertSingleFile(file,idx+1)
        
            
def convertSingleFile(file,idx):
    currentFile.set(file)
    inputFile = file
    outputFile = generateOutputFilePath(inputFile)
    print("file name")
    print(inputFile)
    
    cmd = [
        "ffmpeg", "-y", "-i", inputFile, "-c:v", "libx264", "-crf", "24", "-movflags", "+faststart", "-c","copy", outputFile,
    ]

    ff = FfmpegProgress(cmd)
    for progress in ff.run_command_with_progress():
        progressString.set(f"Completed: {progress}%")
        print(f"{progress}/100")
    totalComplete.set(f"{idx}/{len(files)} files converted")

def generateOutputFilePath(inputPath):
    fileNameTemp = os.path.basename(inputPath).split('/')[-1]
    tmp = fileNameTemp.replace(".dav",".mp4")
    outputFileName = os.path.join(output_folder_path.get(),tmp)
    print(outputFileName)
    return outputFileName

            
def check_ffmpeg():
    """
    Check if ffmpeg is installed.
    """
    return check_install('ffmpeg', "-version")         
def check_install(*args):
    try:
        subprocess.check_output(args,
                    stderr=subprocess.STDOUT)
        return True
    except OSError as e:
        return False  

files = []
completedFiles = 0


root = Tk()  # create a root widget
root.title(".dav to .mp4 converter by Monzurul ISLAM")
# root.attributes('-fullscreen',True)
# root.configure(background="yellow")

folder_string = StringVar()
folder_string.set("Please select a folder")
output_folder_string = StringVar()
output_folder_string.set("Please select a folder to save")
totalFiles = StringVar()
totalFiles.set("Total files: 0")
progressString = StringVar()
progressString.set("Completed: 0%")
progressVar = DoubleVar()
progressVar.set(0.0)
currentFile = StringVar()
currentFile.set("Current file: None")
totalComplete = StringVar()


root.geometry("800x500+50+50")  # width x height + x + y

label = Label(master=root,textvariable="asdf")
label.pack()

folder_path = StringVar()
output_folder_path = StringVar()

button2 = Button(text="Browse", command=browse_button,)
button2.pack(pady=4)
lbl1 = Label(master=root, textvariable=folder_string)
lbl1.pack(pady=4)
button2 = Button(text="Scan files", command=scanFiles)
button2.pack(pady=4)
lbl2 = Label(master=root, textvariable=totalFiles)
lbl2.pack(pady=4)
button20 = Button(text="Folder to save", command=folder_to_save_button,)
button20.pack(pady=4)
lbl1 = Label(master=root, textvariable=output_folder_string)
lbl1.pack(pady=4)
button3 = Button(text="Start Converting", command=threading.Thread(target=convertFiles).start)
button3.pack()
lbl3 = Label(master=root, textvariable=currentFile)
lbl3.pack(pady=4)
lbl4 = Label(master=root, textvariable=totalComplete)
lbl4.pack(pady=4)
lbl5 = Label(master=root, textvariable=progressString)
lbl5.pack(pady=4)

root.mainloop()
