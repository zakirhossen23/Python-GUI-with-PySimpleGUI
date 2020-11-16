'''IMAGE VIEWER

PySimpleGUI reads images in PNG, GIF, PPM/PGM format.
JPEGs cannot be shown because tkinter does not naively support these formats.
JPEGs can be converted to PNG format using the Python Imaging Library (PIL)
package prior to viewing them using PySimpleGUI package.

Sample code for conversion from JPEG/JPG to PNGs is hsown in the commented code block below.

extension = values["image_file"].lower().split(".")[-1]
if extension in ["jpg", "jpeg"]:  # JPG file
    new_filename = values["image_file"].replace(extension, "png")
    im = Image.open(values["image_file"])
    im.save(new_filename)
'''

import os.path
import PySimpleGUI as sg

FILE_SELECT_COLUMN_LAYOUT = [
    [sg.Text("Image Folder:")],
    [sg.In(size=(52, 1), enable_events=True, key="-FOLDER-"),
     sg.FolderBrowse(tooltip="Select a folder"),],
    [sg.Text("Images Retrieved: **(PNG/GIF)")],
    [sg.Listbox(values=[], enable_events=True, size=(59, 20), key="-FILE LIST-")],]

IMAGE_VIEWER_COLUMN_LAYOUT = [
    [sg.Text("                             Select an image from list", key="-STATIC_TEXT-",
             font=("Helvetica", 25))],
    [sg.Text(size=(110, 1), key="-IMAGE_FILE-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full Window Layout -----
WINDOW_LAYOUT = [[sg.Column(FILE_SELECT_COLUMN_LAYOUT),
                  sg.VSeperator(), sg.Column(IMAGE_VIEWER_COLUMN_LAYOUT)],
                 [sg.Button("Reset", key="-RESET-"), sg.Button("Exit", key="-Exit-")],]

CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
WINDOW = sg.Window("Image Viewer", WINDOW_LAYOUT, icon=CURRENT_WORKING_DIRECTORY + "\\img_view.ico")

# Run the Event Loop
while True:
    EVENT, VALUES = WINDOW.read()

    # Exit the viewer in the event of close clicked or exit clicked.
    if EVENT in (sg.WIN_CLOSED, "-Exit-"):
        break

    # Restore the window to the initial state on the event of Reset.
    if EVENT == "-RESET-":
        WINDOW["-IMAGE_FILE-"].update('')
        WINDOW["-IMAGE-"].update(filename='')
        WINDOW['-FILE LIST-'].update(values=[])
        WINDOW["-STATIC_TEXT-"].update("                             Select an image from list",
                                       font=("Helvetica", 25))
        WINDOW["-FOLDER-"].update('')

    # Extract the list of image files in the selected folder.
    if EVENT == "-FOLDER-":
        FOLDER = VALUES["-FOLDER-"]
        try:
            # Get list of files in folder
            FILE_LIST = os.listdir(FOLDER)
        except: # pylint: disable=bare-except
            FILE_LIST = []

        FNAMES = [imgfile for imgfile in FILE_LIST
                  if os.path.isfile(os.path.join(FOLDER, imgfile))
                  and imgfile.lower().endswith((".png", ".gif"))]

        WINDOW["-FILE LIST-"].update(FNAMES)

    elif EVENT == "-FILE LIST-": # Display the image selected.
        try:
            FILENAME = os.path.join(
                VALUES["-FOLDER-"], VALUES["-FILE LIST-"][0]
            )
            WINDOW["-IMAGE_FILE-"].update(FILENAME)
            WINDOW["-IMAGE-"].update(filename=FILENAME)
            WINDOW["-STATIC_TEXT-"].update("Image Selected:", font=("Helvetica", 12))

        except: # pylint: disable=bare-except
            pass

WINDOW.close()
