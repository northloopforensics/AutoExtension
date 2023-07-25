#python3 script to walk directory and add file extensions where needed


import os
import PySimpleGUI as sg
import os
import magic
import shutil
import string

mime = magic.Magic(mime=True)
printable = set(string.printable)

#********************* LAND OF FUNCTIONS ***********************

def walk_dirs(input_folder, output_folder):
    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', time_between_frames=100)
    shutil.copytree(src=input_folder,dst=output_folder, dirs_exist_ok=True)
    for root, dirs, files in os.walk(output_folder):      # walks folders and subfolders
        for filename in files:
            newfilename = (str(filename.encode('ascii', errors='ignore').decode('utf-8')))      #   removes nonascii unicode characters for Magic library
            old_path = os.path.join(root,filename)          #   used for the file rename below
            file = os.path.join(root,newfilename)           #   new path without illegal characters
            os.rename(src=old_path,dst=file)                #   rename to path without illegal charcters

            if "." not in file[-6:]:                    #   looks at last 6 characters to see if file extension not present, if not present it checks mime type
                filetype = mime.from_file(file)  
                extension = filetype.split('/')   
                # if 'image' in filetype or 'video' in filetype:      #checks mimetype for file with no extension
                if len(extension[1]) >= 7:                             # if the mimetype descriptor is long it checks here
                    if 'officedocument.presentation' in extension[1]:
                        extension[1] = 'pptx'
                    if 'officedocument.wordprocessing' in extension[1]:
                        extension[1] = 'docx'
                    if 'officedocument.spreadsheet' in extension[1]:
                        extension[1] = 'xlsx'
                file_w_ext = (file + "." + extension[1])
                os.rename(src=file,dst=file_w_ext)
    sg.PopupAnimated(None)
#***************************** GUI-VILLE *********************************************

sg.theme('reddit')  #GUI color scheme

layout = [[sg.Text("AutoExtension", font=('Impact',24))],
        [sg.Text('This tool will locate files without a file extension, identify the file type, and add the appropriate extension.',font=('Arial', 12))],                                                                        #Cutting Tab Window
        [sg.Text('        '), sg.Text('Select Input and Output Directory:', font=('Arial', 12))],
        [sg.Text('        '),sg.Input("INPUT FOLDER - Source data", font=('Arial', 12), key='SOURCE',), sg.FolderBrowse(key='SOURCE'), sg.Text(' '*10)], 
        [sg.Text('')],
        [sg.Text('        '),sg.Input("OUTPUT FOLDER - Save files with added extensions", font=('Arial', 12), key='OUT',), sg.FolderBrowse(key='OUT')],
        [sg.Text('        '),sg.Text('')],
        [sg.Text('')],
        [sg.Text('        '),sg.Button('ADD FILE EXTENSIONS',font=('Arial'), key='Ok')],
        [sg.Text('')],]
        

#******************** BRINGS GUI & FUNCTIONS TOGETHER ********************************


# Create the Window
window = sg.Window('North Loop Consulting', layout, no_titlebar=False, alpha_channel=1, grab_anywhere=False)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    if event == 'Ok':
       walk_dirs(input_folder=values["SOURCE"], output_folder=values['OUT'])
       sg.popup("Process Complete",font=("Arial", 12))
       
 
window.close()