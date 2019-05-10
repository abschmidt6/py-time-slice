from tkinter import filedialog
from tkinter import *
from slicer import Slicer
from os.path import dirname, abspath, join
from os import listdir
import subprocess
from tkinter import font  as tkfont
class GUI():
    def __init__(self):


        # Tkinter initialize
        self.window = Tk()

        # initialize contant member variables
        self.initConstMemberVars()

        # Tkinter window setup
        self.window.title("Py-Time-Slice")
        self.window.geometry('800x800')
        self.window.configure(bg=self.bg_color)

        # Variables to be passed to the Slicer
        self.folder_selected = None
        self.reverse = StringVar()
        self.reverse.set("false")
        self.num_imgs = 0
        self.num_slices = 0
        self.mode = StringVar()
        self.mode.set("linear")

        # Create widgets to build GUI
        self.createWidgets()

    def initConstMemberVars(self):
        self.title_font = tkfont.Font(family='Arial', size=16, weight="bold", slant="italic")
        self.subtitle_font = tkfont.Font(family='Arial', size=12, weight="bold")
        self.bg_color = "white"
        self.text_color = "#1133bb"

    def createWidgets(self):
        # --- CREATE MAIN frame TO HOLD ALL OTHERS ---
        self.main_frame = Frame(self.window, bg = self.bg_color)
        self.main_frame.pack(expand=YES, fill=BOTH)

        # --- CREATE BANNER frame AND FILL WITH IMAGE ---
        self.banner_frame = Frame(self.main_frame, bg=self.bg_color)
        # load banner image
        imgpath = join(dirname(abspath(__file__)), "banner.PNG")
        logo = PhotoImage(file = imgpath)
        logo_lbl = Label(self.banner_frame, image=logo)
        # why do I need this line? --> Python and tkinter references and garbage collection
        # [just don't change it]
        logo_lbl.image = logo
        logo_lbl.pack()
        self.banner_frame.pack(expand=NO, fill=X)

        # --- CREATE PADDING frame AND LEAVE EMPTY ---
        self.pad_frame = Frame(self.main_frame, bg=self.bg_color,
            width=600,
            height=40
        )
        self.pad_frame.pack()

        # --- CREATE CONTENT frame FOR DIRECTORY SELECTION AND OPTIONS ---
        self.content_frame = Frame(self.main_frame, bg=self.bg_color,
            width=600
        )
        self.content_frame.pack(fill=Y)

        # --- CREATE DIRECTORY frame TO SELECT DIRECTORY---
        self.dir_frame = Frame(self.content_frame, bg=self.bg_color,
            width=300
        )
        # Updatable labels
        self.curr_dir_lbl = StringVar()
        self.curr_dir_lbl.set("")
        self.num_imgs_lbl = StringVar()
        self.num_imgs_lbl.set("")
        # Select the directory
        Label(self.dir_frame, text="1. Choose an input folder",
            font=self.title_font,
            width=25,
            bg=self.bg_color
        ).pack(anchor=W)
        Button(self.dir_frame, text="Select Folder",
            command=self.selectDir,
            padx=20
        ).pack()
        Label(self.dir_frame, textvariable=self.curr_dir_lbl,
            bg=self.bg_color
        ).pack()
        Label(self.dir_frame, textvariable=self.num_imgs_lbl,
            bg=self.bg_color
        ).pack()
        self.dir_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # --- CREATE OPTION frame FOR OPTIONS---
        self.opt_frame = Frame(self.content_frame, bg=self.bg_color,
            width=600
        )
        Label(self.opt_frame, text="2. Select Options",
            font=self.title_font,
            width=25,
            bg=self.bg_color
        ).pack()
        Label(self.opt_frame, text="Image slicing mode:",
            bg=self.bg_color,
            font=self.subtitle_font,
            fg=self.text_color
        ).pack(anchor=W)
        Radiobutton(self.opt_frame, text="Linear",
            indicatoron=1,
            value="linear",
            variable=self.mode,
            bg=self.bg_color
        ).pack(anchor=W)
        Radiobutton(self.opt_frame, text="Convex",
            indicatoron=1,
            value="convex",
            variable=self.mode,
            bg=self.bg_color
        ).pack(anchor=W)
        Radiobutton(self.opt_frame, text="Concave",
            indicatoron=1,
            value="concave",
            variable=self.mode,
            bg=self.bg_color
        ).pack(anchor=W)

        Label(self.opt_frame, text="Image ordering mode:",
            bg=self.bg_color,
            font=self.subtitle_font,
            fg=self.text_color
        ).pack(anchor=W)
        Radiobutton(self.opt_frame, text="Normal",
            indicatoron=1,
            value="false",
            variable=self.reverse,
            bg=self.bg_color
        ).pack(anchor=W)
        Radiobutton(self.opt_frame, text="Reverse",
            indicatoron=1,
            value="true",
            variable=self.reverse,
            bg=self.bg_color
        ).pack(anchor=W)

        Label(self.opt_frame, text="Number of slices:",
            bg=self.bg_color,
            font=self.subtitle_font,
            fg=self.text_color
        ).pack(anchor=W)

        Label(self.opt_frame, text="Choose how many images to use",
            bg=self.bg_color,
        ).pack(anchor=W)
        self.num_slices_entry = Entry(self.opt_frame).pack(anchor=W)
        Label(self.opt_frame, text="If no number is entered, all images will be used",
            bg=self.bg_color,
        ).pack(anchor=W)



        self.opt_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # --- CREATE RUN frame TO RUN PROGFRAM ---
        self.run_frame = Frame(self.main_frame)
        Label(self.run_frame, text="3. Run",
            width=50,
            font=self.title_font,
            bg=self.bg_color
        ).pack()
        self.run_frame.pack()

        # --- CREATE FOOTER frame FOR CREDITS---
        self.footer_frame = Frame(self.main_frame, bg=self.bg_color, width=600, height=100)
        Label(self.footer_frame, text="Created by Andrew Schmidt").pack()
        self.footer_frame.pack(side=BOTTOM)

    def selectDir(self):
        self.folder_selected = filedialog.askdirectory()
        self.curr_dir_lbl.set("{}".format((self.folder_selected)))

        output = listdir(self.folder_selected)
        img_names = [ elem for elem in output if (".jpg" in elem.lower() and "slicer" not in elem.lower())]
        self.num_imgs_lbl.set("{} eligible images in this folder".format((str(len(img_names)))))

    def runSlicer(self):
        self.num_slices = int(self.num_slices_entry.get())
    def mainloop(self):
        self.window.mainloop()

app = GUI()
app.mainloop()