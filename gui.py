from tkinter import filedialog
from tkinter import *
from slicer import Slicer
from os.path import dirname, abspath, join
from os import listdir
import subprocess
class GUI():
    def __init__(self):
        self.window = Tk()
        self.window.title("Py-Time-Slice")
        self.window.geometry('800x800')
        self.folder_selected = None
        self.createWidgets()


    def createWidgets(self):
        # Setup Frames
        banner_frame = Frame(self.window).pack()
        content_frame = Frame(self.window).pack(side = "bottom")

        # load banner image
        imgpath = join(dirname(abspath(__file__)), "banner.PNG")
        logo = PhotoImage(file = imgpath)
        logo_lbl = Label(banner_frame, image=logo)
        # why do I need this line?
        # Python and tkninter references and garbage collection
        # [just don't change it]
        logo_lbl.image = logo
        logo_lbl.pack()

        # Below Banner content
        # Updatable labels
        self.curr_dir_lbl = StringVar()
        self.curr_dir_lbl.set("Chosen folder:")
        self.num_imgs_lbl = StringVar()
        self.num_imgs_lbl.set("")
        # Select the directory
        Label(content_frame, text="Choose an input directory").pack()
        Button(content_frame, text="Select Folder", command=self.selectDir).pack()
        Label(content_frame, textvariable=self.curr_dir_lbl).pack()
        Label(content_frame, textvariable=self.num_imgs_lbl).pack()


    def selectDir(self):
        self.folder_selected = filedialog.askdirectory()
        self.curr_dir_lbl.set("Chosen folder: {}".format((self.folder_selected)))

        output = listdir(self.folder_selected)
        img_names = [ elem for elem in output if (".jpg" in elem.lower() and "slicer" not in elem.lower())]
        self.num_imgs_lbl.set("{} eligible images in this folder".format((str(len(img_names)))))

    def mainloop(self):
        self.window.mainloop()

app = GUI()
app.mainloop()