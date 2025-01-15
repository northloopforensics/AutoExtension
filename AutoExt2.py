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

            if "." not in file[-6:]:  # looks at last 6 characters to see if file extension not present, if not present it checks mime type
                filetype = mime.from_file(file)
                extension = filetype.split('/')
                if len(extension[1]) >= 7:  # if the mimetype descriptor is long it checks here
                    if 'officedocument.presentation' in extension[1]:
                        extension[1] = 'pptx'
                    elif 'officedocument.wordprocessing' in extension[1]:
                        extension[1] = 'docx'
                    elif 'officedocument.spreadsheet' in extension[1]:
                        extension[1] = 'xlsx'
                    elif 'application' in extension[0] and ('x-executable' in extension[1] or 'x-dosexec' in extension[1]):
                        extension[1] = 'exe'
                    elif 'application/pdf' in filetype:
                        extension[1] = 'pdf'
                    elif 'text/plain' in filetype:
                        extension[1] = 'txt'
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
ctk.CTkLabel(app, text="This tool will locate files without a file extension, identify the file type, and add the appropriate extension.", font=('Arial', 12)).pack(pady=10)

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
