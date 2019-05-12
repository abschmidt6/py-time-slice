from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from slicer import Slicer
from os.path import dirname, abspath, join
from os import listdir
import subprocess
from tkinter import font  as tkfont
import threading
import time
class GUI():
    def __init__(self):


        # Tkinter initialize
        self.root = Tk()

        # initialize contant member variables
        self.initConstMemberVars()

        # Tkinter window setup
        self.root.title("Py-Time-Slice")
        self.root.geometry('685x850')
        self.root.configure(bg=self.bg_color)

        self.canvas = Canvas(self.root, borderwidth=0, bg=self.bg_color)
        self.main_frame = Frame(self.root, bg=self.bg_color)
        self.vsb = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.hsb = Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")

        self.main_frame.bind("<Configure>", self.onFrameConfigure)
        self.main_frame.bind_all("<MouseWheel>", self.on_mousewheel)

        self.canvas.create_window((0,0), window=self.main_frame,
                                    anchor = "nw",
                                    tags="self.main_frame")

        self.canvas.pack(side="top", fill="both", expand=True)



        # Variables to be passed to the Slicer
        self.folder_selected = None
        self.reverse = BooleanVar()
        self.reverse.set(False)
        self.num_imgs = 0
        self.num_slices = 0
        self.mode = StringVar()
        self.mode.set("linear")
        self.img_ext = ".jpg"
        self.curve_depth = 1

        # Create widgets to build GUI
        self.createWidgets()

    def initConstMemberVars(self):
        self.title_font = tkfont.Font(family='Arial', size=16, weight="bold", slant="italic")
        self.subtitle_font = tkfont.Font(family='Arial', size=12, weight="bold")
        self.bg_color = "white"
        self.text_color = "#1133bb"
        self.default_out_dir_lbl = "Ouput folder defaults to same as input folder"

    def createWidgets(self):

        self.createBannerFrame()
        self.createPaddingFrame()
        self.createContentFrame()
        self.createDirFrame()
        self.createOptFrame()
        self.createRunFrame()
        self.createFooterFrame()

    def createBannerFrame(self):
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

    def createPaddingFrame(self):
        # --- CREATE PADDING frame AND LEAVE EMPTY ---
        self.pad_frame = Frame(self.main_frame, bg=self.bg_color,
            width=600,
            height=40
        )
        self.pad_frame.pack()

    def createContentFrame(self):
        # --- CREATE CONTENT frame FOR DIRECTORY SELECTION AND OPTIONS ---
        self.content_frame = Frame(self.main_frame, bg=self.bg_color,
            width=600
        )
        self.content_frame.pack(fill=Y)

    def createDirFrame(self):
        # --- CREATE DIRECTORY frame TO SELECT DIRECTORY---
        self.dir_frame = Frame(self.content_frame, bg=self.bg_color,
            width=300
        )
        # Updatable labels
        self.curr_dir_lbl = StringVar()
        self.curr_dir_lbl.set("")
        self.num_imgs_lbl = StringVar()
        self.num_imgs_lbl.set("")
        self.out_dir_lbl = StringVar()
        self.out_dir_lbl.set(self.default_out_dir_lbl)

        # Select the directory
        Label(self.dir_frame, text="1. Choose folders",
            font=self.title_font,
            width=25,
            bg=self.bg_color
        ).pack(anchor=W)
        Button(self.dir_frame, text="Select Input Folder",
            command=self.selectDir,
            padx=20,
            pady=5
        ).pack()
        Label(self.dir_frame, textvariable=self.curr_dir_lbl,
            bg=self.bg_color,
        ).pack()
        Label(self.dir_frame, textvariable=self.num_imgs_lbl,
            bg=self.bg_color,
        ).pack()
        Label(self.dir_frame, text="", bg=self.bg_color, pady=10).pack()
        Button(self.dir_frame, text="Select Output Folder",
            command=self.selectOutDir,
            padx=20,
            pady=5
        ).pack()
        Label(self.dir_frame, textvariable=self.out_dir_lbl,
            bg=self.bg_color
        ).pack()
        self.dir_frame.pack(side=LEFT, fill=BOTH, expand=YES)

    def createOptFrame(self):
        # --- CREATE OPTION frame FOR OPTIONS---
        self.opt_frame = Frame(self.content_frame, bg=self.bg_color,
            width=600
        )
        Label(self.opt_frame, text="2. Select Options",
            font=self.title_font,
            width=25,
            bg=self.bg_color
        ).pack()

        # Options for image slicing mode
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

        # Options for image ordering mode
        Label(self.opt_frame, text="Image ordering mode:",
            bg=self.bg_color,
            font=self.subtitle_font,
            fg=self.text_color
        ).pack(anchor=W)
        Radiobutton(self.opt_frame, text="Normal",
            indicatoron=1,
            value=False,
            variable=self.reverse,
            bg=self.bg_color
        ).pack(anchor=W)
        Radiobutton(self.opt_frame, text="Reverse",
            indicatoron=1,
            value=True,
            variable=self.reverse,
            bg=self.bg_color
        ).pack(anchor=W)

        # Options for number of slices
        Label(self.opt_frame, text="Number of slices:",
            bg=self.bg_color,
            font=self.subtitle_font,
            fg=self.text_color
        ).pack(anchor=W)
        Label(self.opt_frame, text="Choose how many images to use",
            bg=self.bg_color,
        ).pack(anchor=W)
        self.num_slices_entry = Entry(self.opt_frame)
        self.num_slices_entry.pack(anchor=W)
        Label(self.opt_frame, text="If no number is entered, all images will be used",
            bg=self.bg_color,
        ).pack(anchor=W)

        # Pack frame
        self.opt_frame.pack(side=LEFT, fill=BOTH, expand=YES)


    def createRunFrame(self):
        # --- CREATE RUN frame TO RUN PROGFRAM ---
        self.run_frame = Frame(self.main_frame)
        Label(self.run_frame, text="3. Run",
            width=50,
            font=self.title_font,
            bg=self.bg_color
        ).pack()
        Button(self.run_frame, text="Run Py-Time-Slice",
            command=self.runSlicer,
            padx=20,
            pady=5
        ).pack(fill=X)

        self.curr_img_lbl = StringVar()
        self.curr_img_lbl.set("")

        Label(self.run_frame, textvariable=self.curr_img_lbl,
            bg=self.bg_color,
        ).pack(fill=X)

        self.progress = ttk.Progressbar(self.run_frame, orient="horizontal",
                                        mode="determinate")
        self.progress.pack(fill=X)

        self.run_frame.pack()

    def createFooterFrame(self):
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
        self.num_imgs = len(img_names)

        if self.out_dir_lbl.get() == self.default_out_dir_lbl:
            self.out_dir_lbl.set("{}".format((self.folder_selected)))

    def selectOutDir(self):
        self.out_folder_selected = filedialog.askdirectory()
        self.out_dir_lbl.set("{}".format((self.out_folder_selected)))

    def runSlicer(self):
        # DEBUG:
        self.printSlicerVars()

        num_iters = self.num_slices_entry.get()
        if not num_iters:
            num_iters = self.num_imgs
        else:
            num_iters = int(num_iters)

        slicer = Slicer(
            in_dir = self.curr_dir_lbl.get(),
            out_dir = self.out_dir_lbl.get(),
            img_ext = self.img_ext,
            mode = self.mode.get(),
            reverse = self.reverse.get(),
            curve_depth = self.curve_depth,
            num_slices = num_iters
        )
        self.progress["value"] = 0
        self.progress["maximum"] = num_iters

        slice_thread = threading.Thread(target=slicer.slice)
        slice_thread.start()

        prog_thread = threading.Thread(target=self.watchProgress, args=(slicer, num_iters))
        prog_thread.start()

    def watchProgress(self, slicer, num_iters):
        while True:
            info = slicer.getThreadUpdateInfo()
            self.curr_img_lbl.set("Processing: " + str(info[0]))
            self.progress["value"] = info[1]


            if info[1] == num_iters:
                break

            time.sleep(.1)

    def printSlicerVars(self):
        print("in_dir:\t{}".format((self.curr_dir_lbl.get())))
        print("out_dir\t{}".format((self.out_dir_lbl.get())))
        print("img_ext\t{}".format((self.img_ext)))
        print("mode\t{}".format((self.mode.get())))
        print("reverse\t{}".format((self.reverse.get())))
        print("curve_depth\t{}".format((self.curve_depth)))
        print("num_slices\t{}".format((self.num_slices_entry.get())))
        print("num_imgs\t{}".format((self.num_imgs)))

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def mainloop(self):
        self.root.mainloop()

app = GUI()
app.mainloop()