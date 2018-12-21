import subprocess
from PIL import Image
class Slicer:

    def __init__(self, dir_name, img_ext, mode):
        self.dir_name = dir_name    # path
        self.img_ext = img_ext      # jpg works so far
        self.mode = mode            # simple, concave, convex
        self.image_names = []
        self.num_images = 0
        self.img_size = (0, 0)
        self.img_mode = ""
        self.col_width = 0

    def getImageNames(self):
        process = subprocess.run(["dir", self.dir_name + "*" + self.img_ext], stdout=subprocess.PIPE, shell=True)
        if process.returncode != 0:
            print("ERROR::   Image names could not be selected from directory")
            print("Good Bye")
            exit()

        self.img_names = [ elem for elem in process.stdout.decode().split() if self.img_ext in elem ]
        self.num_imgs = len(self.img_names)

    def getImageSize(self):
        tmp_img  = Image.open(self.dir_name + self.img_names[0])
        self.img_size = tmp_img.size
        self.img_mode = tmp_img.mode
        tmp_img.close()

        self.col_width =  int(self.img_size[0] / self.num_imgs)

    def slice(self):
        self.getImageNames()
        self.getImageSize()

        final_img = Image.new(self.img_mode, self.img_size)
        l_col_boundary = 0
        r_col_boundary = self.col_width
        for img_name in self.img_names:
            # Make sure image can open
            try:
                img  = Image.open(self.dir_name + img_name)
                print("Processing: " + str(img_name))
            except IOError:
                print("ERROR::   Image: " + img_name + " could not be opened")
                print("Good Bye")
                exit()

            for i in range(l_col_boundary, r_col_boundary):
                for j in range(self.img_size[1]):
                    final_img.putpixel((i,j), img.getpixel((i,j)))

            l_col_boundary = r_col_boundary
            r_col_boundary = min(r_col_boundary + self.col_width, self.img_size[0])

        final_img.save(self.dir_name + "Slice-output" + self.img_ext)
