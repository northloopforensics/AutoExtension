#python3 script to walk directory and strip first or last bytes from each file under that directory
#It also adds 'AMENDED' to the front of the file name so you know what is new
#This does not look at file headers. It is not smart. 
#
#   Tool workflow
#  1. ID a target folder containing files that need bytes removed
#   |
#  2. Choose an output folder to store changed files
#   |
#  3. Select # of bytes to remove from start OR end of files
#   |
#   <OPTIONAL>
#   |
#  4. Preview window to see raw binary of a sample file

import os
import PySimpleGUI as sg
import os
import magic
import shutil

mime = magic.Magic(mime=True)


#********************* LAND OF FUNCTIONS ***********************

def walk_dirs(input_folder, output_folder):
    shutil.copytree(src=input_folder,dst=output_folder, dirs_exist_ok=True)
    for root, dirs, files in os.walk(output_folder):      # walks folders and subfolders
        for filename in files:
            file = os.path.join(root,filename)
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
 
#***************************** GUI-VILLE *********************************************

sg.theme('lightgray6')  #GUI color scheme

layout = [[sg.Text("AutoExtension", font=('Impact',24))],
        [sg.Text('This tool will locate files without a file extension, identify the file type, and add the appropriate extension.',font=('Arial', 12))],                                                                        #Cutting Tab Window
        [sg.Text('        '), sg.Text('Select Input and Output Directory:', font=('Arial', 12))],
        [sg.Text('        '),sg.Input("INPUT FOLDER - Source data", font=('Arial', 12), key='SOURCE',), sg.FolderBrowse(key='SOURCE'), sg.Text(' '*10)], 
        [sg.Text('')],
        [sg.Text('        '),sg.Input("OUTPUT FOLDER - Save files with added extensions", font=('Arial', 12), key='OUT',), sg.FolderBrowse(key='OUT')],
        [sg.Text('        '),sg.Text('')],
        [sg.Text('')],
        [sg.Text('        '),sg.Button('ADD FILE EXTENSIONS',font=('Arial-bold'), key='Ok')],
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