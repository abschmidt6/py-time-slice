from tkinter import filedialog
from tkinter import *
from slicer import Slicer
from os.path import dirname, abspath, join
from os import listdir
import subprocess
from tkinter import font  as tkfont
class GUI():
    def __init__(self):
        self.window = Tk()
        self.window.title("Py-Time-Slice")
        self.window.geometry('800x800')
        self.folder_selected = None
        self.title_font = tkfont.Font(family='Arial', size=16, weight="bold", slant="italic")
        self.createWidgets()


    def createWidgets(self):
        # --- CREATE MAIN CONTAINER TO HOLD ALL OTHERS ---
        self.main_container = Frame(self.window, background = "white")
        self.main_container.pack(expand=YES, fill=BOTH)

        # --- CREATE BANNER CONTAINER AND FILL WITH IMAGE ---
        self.banner_container = Frame(self.main_container, background="white")
        # load banner image
        imgpath = join(dirname(abspath(__file__)), "banner.PNG")
        logo = PhotoImage(file = imgpath)
        logo_lbl = Label(self.banner_container, image=logo)
        # why do I need this line? --> Python and tkinter references and garbage collection
        # [just don't change it]
        logo_lbl.image = logo
        logo_lbl.pack()
        self.banner_container.pack(expand=NO, fill=X)

        # --- CREATE PADDING CONTAINER AND LEAVE EMPTY ---
        self.pad_container = Frame(self.main_container,  background="white", width=600, height=40)
        self.pad_container.pack()

        # --- CREATE CONTENT CONTAINER FOR DIRECTORY SELECTION AND OPTIONS ---
        self.content_container = Frame(self.main_container, background="white", width=600)
        self.content_container.pack(fill=Y)

        # --- CREATE DIRECTORY CONTAINER TO SELECT DIRECTORY---
        self.dir_container = Frame(self.content_container)
        # Updatable labels
        self.curr_dir_lbl = StringVar()
        self.curr_dir_lbl.set("")
        self.num_imgs_lbl = StringVar()
        self.num_imgs_lbl.set("")
        # Select the directory
        Label(self.dir_container, text="1. Choose an input folder", font=self.title_font, width = 25).pack()
        Button(self.dir_container, text="Select Folder", command=self.selectDir).pack()
        Label(self.dir_container, textvariable=self.curr_dir_lbl).pack()
        Label(self.dir_container, textvariable=self.num_imgs_lbl).pack()
        self.dir_container.pack(side=LEFT)

        # --- CREATE OPTION CONTAINER FOR OPTIONS---
        self.opt_container = Frame(self.content_container)
        Label(self.opt_container, text="2. Select Options", font=self.title_font, width=25).pack()
        self.opt_container.pack(side=LEFT)

        # --- CREATE RUN CONTAINER TO RUN PROGFRAM ---
        self.run_container = Frame(self.main_container)
        Label(self.run_container, text="3. Run", width=50, font=self.title_font).pack()
        self.run_container.pack()

        # --- CREATE FOOTER CONTAINER FOR CREDITS---
        self.footer_container = Frame(self.main_container, background="white", width=600, height=100)
        Label(self.footer_container, text="Created by Andrew Schmidt").pack()
        self.footer_container.pack(side=BOTTOM)

    def selectDir(self):
        self.folder_selected = filedialog.askdirectory()
        self.curr_dir_lbl.set("{}".format((self.folder_selected)))

        output = listdir(self.folder_selected)
        img_names = [ elem for elem in output if (".jpg" in elem.lower() and "slicer" not in elem.lower())]
        self.num_imgs_lbl.set("{} eligible images in this folder".format((str(len(img_names)))))

    def mainloop(self):
        self.window.mainloop()

app = GUI()
app.mainloop()