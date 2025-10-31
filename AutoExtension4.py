#python3 

import os
import customtkinter as ctk
import magic
import shutil
import string
from tkinter import filedialog, messagebox

mime = magic.Magic(mime=True)
printable = set(string.printable)

#********************* LAND OF FUNCTIONS ***********************

def walk_dirs(input_folder, output_folder):
    shutil.copytree(src=input_folder, dst=output_folder, dirs_exist_ok=True)
    for root, dirs, files in os.walk(output_folder):  # walks folders and subfolders
        for filename in files:
            newfilename = (str(filename.encode('ascii', errors='ignore').decode('utf-8')))  # removes nonascii unicode characters for Magic library
            old_path = os.path.join(root, filename)  # used for the file rename below
            file = os.path.join(root, newfilename)  # new path without illegal characters
            os.rename(src=old_path, dst=file)  # rename to path without illegal characters

            if "." not in file[-6:] or file.endswith('.unknown'):  # looks at last 6 characters to see if file extension not present or if extension is .unknown, if so it checks mime type
                filetype = mime.from_file(file)
                extension = filetype.split('/')
                if len(extension[1]) >= 4:  # if the mimetype descriptor is long it checks here
                    # Office Docs
                    if 'officedocument.presentation' in extension[1]:
                        extension[1] = 'pptx'
                    elif 'officedocument.wordprocessing' in extension[1]:
                        extension[1] = 'docx'
                    elif 'officedocument.spreadsheet' in extension[1]:
                        extension[1] = 'xlsx'
                    elif 'application/pdf' in filetype:
                        extension[1] = 'pdf'
                    elif 'csv' in filetype:
                        extension[1] = 'csv'
                    elif 'richtext' in filetype or 'rtf' in filetype:
                        extension[1] = 'rtf'
                    elif 'xml' in filetype:
                        extension[1] = 'xml'
                    elif 'application/msword' in filetype:
                        extension[1] = 'doc'
                    elif 'application/vnd.ms-excel' in filetype:
                        extension[1] = 'xls'
                    elif 'application/vnd.ms-powerpoint' in filetype:
                        extension[1] = 'ppt'
                    elif 'text/plain' in filetype:
                        extension[1] = 'txt'
                    # Media
                    elif 'image/webp' in filetype:
                        extension[1] = 'webp'
                    elif 'audio/mpeg' in filetype:
                        extension[1] = 'mp3'
                    elif 'audio/wav' in filetype:
                        extension[1] = 'wav'
                    elif 'video/mp4' in filetype:
                        extension[1] = 'mp4'
                    elif 'video/quicktime' in filetype:
                        extension[1] = 'mov'
                    # Archives
                    elif 'application/zip' in filetype:
                        extension[1] = 'zip'
                    elif 'application/x-rar' in filetype:
                        extension[1] = 'rar'
                    elif 'application/x-7z-compressed' in filetype:
                        extension[1] = '7z'
                    # Code
                    elif 'text/x-python' in filetype:
                        extension[1] = 'py'
                    elif 'text/html' in filetype:
                        extension[1] = 'html'
                    elif 'text/javascript' in filetype:
                        extension[1] = 'js'
                    # Images
                    elif 'image/jpeg' in filetype:
                        extension[1] = 'jpg'
                    elif 'image/png' in filetype:
                        extension[1] = 'png'
                    elif 'image/gif' in filetype:
                        extension[1] = 'gif'
                    elif 'image/svg+xml' in filetype:
                        extension[1] = 'svg'
                    # Executables
                    elif 'application' in extension[0] and ('x-executable' in extension[1] or 'x-dosexec' in extension[1]):
                        extension[1] = 'exe'
                    else:
                        # If no specific match was found above
                        if 'octet-stream' in filetype:
                            extension[1] = 'bin'
                        else:
                            extension[1] = 'unknown'
                
                # Handle renaming for files with .unknown extension
                if file.endswith('.unknown'):
                    # Remove the .unknown extension and add the detected extension
                    file_without_unknown = file[:-8]  # Remove '.unknown'
                    file_w_ext = (file_without_unknown + "." + extension[1])
                else:
                    # For files without extension, just add the extension
                    file_w_ext = (file + "." + extension[1])
                
                os.rename(src=file, dst=file_w_ext)

#***************************** GUI-VILLE *********************************************

def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_entry.delete(0, ctk.END)
    input_folder_entry.insert(0, folder_selected)

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, ctk.END)
    output_folder_entry.insert(0, folder_selected)

def start_process():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    walk_dirs(input_folder=input_folder, output_folder=output_folder)
    messagebox.showinfo("Process Complete", "File extensions have been added successfully.")

app = ctk.CTk()
app.title("AutoExtension")
app.geometry("600x400")

ctk.CTkLabel(app, text="AutoExtension", font=('Impact', 24)).pack(pady=10)
ctk.CTkLabel(app, text="This tool will locate files without a file extension found in the input directory, identify the file type, and add the appropriate extension to copied files in the output directory.", font=('Arial', 12),wraplength=550).pack(pady=10)

input_frame = ctk.CTkFrame(app)
input_frame.pack(pady=10, padx=10, fill="x")

ctk.CTkLabel(input_frame, text="Select Input Directory:", font=('Arial', 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
input_folder_entry = ctk.CTkEntry(input_frame, width=400, font=('Arial', 12))
input_folder_entry.grid(row=1, column=0, padx=5, pady=5)
ctk.CTkButton(input_frame, text="Browse", command=select_input_folder).grid(row=1, column=1, padx=5, pady=5)

output_frame = ctk.CTkFrame(app)
output_frame.pack(pady=10, padx=10, fill="x")

ctk.CTkLabel(output_frame, text="Select Output Directory:", font=('Arial', 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
output_folder_entry = ctk.CTkEntry(output_frame, width=400, font=('Arial', 12))
output_folder_entry.grid(row=1, column=0, padx=5, pady=5)
ctk.CTkButton(output_frame, text="Browse", command=select_output_folder).grid(row=1, column=1, padx=5, pady=5)

ctk.CTkButton(app, text="ADD FILE EXTENSIONS", font=('Arial-bold', 12), command=start_process).pack(pady=20)

app.mainloop()