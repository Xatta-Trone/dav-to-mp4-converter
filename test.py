import glob
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from tkinter import *
from tkinter import filedialog, messagebox
from ffmpeg_progress_yield import FfmpegProgress
import os


def scanFiles():
    if folder_path.get() == "":
        messagebox.showerror(title="Error!!", message="Please select a folder first.")
    files.clear()
    for filename in glob.iglob(folder_path.get() + '/**/**', recursive=True):
        if filename.endswith('.dav'):
            files.insert(0, filename)
    totalFiles.set(f"Total files: {len(files)}")
    totalComplete.set(f"{completedFiles}/{len(files)} files converted")
    print(files)


def browse_button():
    filename = filedialog.askdirectory()
    if len(filename) > 0:
        folder_path.set(filename)
        folder_string.set(folder_path.get())
    else:
        folder_string.set("Please select a folder")
    print("filename")
    print(filename)
    print("filename")


def folder_to_save_button():
    filename = filedialog.askdirectory()
    if len(filename) > 0:
        output_folder_path.set(filename)
        output_folder_string.set(output_folder_path.get())
    else:
        folder_string.set("Please select a folder to save")
    print("filename")
    print(filename)
    print("filename")


def convertFiles():
    if not check_ffmpeg():
        messagebox.showerror(title="Error!!", message="Please install ffmpeg first")
    elif output_folder_path.get() == "":
        messagebox.showerror(title="Error!!", message="Please select a folder to save.")
    else:
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [executor.submit(convertSingleFile, file, idx + 1) for idx, file in enumerate(files)]
            for future in futures:
                future.result()


def convertSingleFile(file, idx):
    currentFile.set(file)
    inputFile = file
    outputFile = generateOutputFilePath(inputFile)
    print("file name")
    print(inputFile)

    cmd = [
        "ffmpeg", "-y", "-i", inputFile, "-c:v", "libx264", "-c:a", "aac", "-crf", "28", "-preset", "fast", "-movflags", "+faststart", "-sn", outputFile,
    ]

    ff = FfmpegProgress(cmd)
    for progress in ff.run_command_with_progress():
        progressString.set(f"Completed: {progress}%")
        print(f"{progress}/100")
    global completedFiles
    completedFiles += 1
    totalComplete.set(f"{completedFiles}/{len(files)} files converted")


def generateOutputFilePath(inputPath):
    p = inputPath
    q = folder_path.get()
    r = output_folder_path.get()

    result = p.replace('\\', '/').replace(q, r).replace(".dav", ".mp4").replace('/', '\\')

    create_directory(os.path.dirname(result))
    return result


def check_ffmpeg():
    return check_install('ffmpeg', "-version")


def check_install(*args):
    try:
        subprocess.check_output(args, stderr=subprocess.STDOUT)
        return True
    except OSError:
        return False


def create_directory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' created successfully")
    except OSError as e:
        print(f"Error: {e}")


files = []
completedFiles = 0

root = Tk()
root.title(".dav to .mp4 converter by Monzurul ISLAM")

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

root.geometry("800x500+50+50")

label = Label(master=root, text="Select Folder")
label.pack()

folder_path = StringVar()
output_folder_path = StringVar()

button2 = Button(text="Browse", command=browse_button)
button2.pack(pady=4)
lbl1 = Label(master=root, textvariable=folder_string)
lbl1.pack(pady=4)
button2 = Button(text="Scan files", command=scanFiles)
button2.pack(pady=4)
lbl2 = Label(master=root, textvariable=totalFiles)
lbl2.pack(pady=4)
button20 = Button(text="Folder to save", command=folder_to_save_button)
button20.pack(pady=4)
lbl1 = Label(master=root, textvariable=output_folder_string)
lbl1.pack(pady=4)
button3 = Button(text="Start Converting", command=lambda: threading.Thread(target=convertFiles).start())
button3.pack()
lbl3 = Label(master=root, textvariable=currentFile)
lbl3.pack(pady=4)
lbl4 = Label(master=root, textvariable=totalComplete)
lbl4.pack(pady=4)
lbl5 = Label(master=root, textvariable=progressString)
lbl5.pack(pady=4)

root.mainloop()
