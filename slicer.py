import subprocess
from PIL import Image
class Slicer:

    def __init__(self, dir_name, img_ext, mode, reverse = False, curve_depth = 1):
        self.dir_name = dir_name    # path
        self.img_ext = img_ext      # jpg works so far
        self.mode = mode            # simple, concave, convex
        self.reverse = reverse      # True or False
        self.image_names = []
        self.num_imgs = 0
        self.img_size = (0, 0)
        self.img_mode = ""
        self.col_width = 0
        self.curve_depth = curve_depth

    def getImageNames(self):
        process = subprocess.run(["dir", self.dir_name + "*" + self.img_ext], stdout=subprocess.PIPE, shell=True)
        if process.returncode != 0:
            print("ERROR::   Image names could not be selected from directory")
            print("Good Bye")
            exit()

        self.img_names = [ elem for elem in process.stdout.decode().split() if ((self.img_ext in elem) and ("Slicer" not in elem)) ]
        self.img_names.sort()
        self.num_imgs = len(self.img_names)

    def getImageSize(self):
        tmp_img  = Image.open(self.dir_name + self.img_names[0])
        self.img_size = tmp_img.size
        self.img_mode = tmp_img.mode
        tmp_img.close()


    def slice(self):
        self.getImageNames()
        self.getImageSize()

        if self.reverse:
            self.img_names.sort(reverse = True)

        if self.mode == "simple":
            self.simpleSlice()
        elif self.mode == "convex":
            self.warpedSlice(self.getConvexFactors())
        elif self.mode == "concave":
            self.warpedSlice(self.getConcaveFactors())
        else:
            print("ERROR::    Invalid Mode")
            print("Good Bye")
            exit()


    def simpleSlice(self):
        col_width =  int(self.img_size[0] / self.num_imgs)

        final_img = Image.new(self.img_mode, self.img_size)
        l_col_boundary = 0
        r_col_boundary = col_width
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
            r_col_boundary = min(r_col_boundary + col_width, self.img_size[0])

        final_img.save(self.dir_name + "Slicer-simple-output" + self.img_ext)

    def warpedSlice(self, factors=[]):
        if len(factors) == 0:
            print("ERROR::    Factors could not be obtained")
            print("Good Bye")
            exit()

        final_img = Image.new(self.img_mode, self.img_size)
        l_col_boundary = 0
        r_col_boundary = int(factors[0] * self.img_size[0])
        factor_counter = 0
        for img_name in self.img_names:
            # Make sure image can open
            factor_counter += 1
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
            if factor_counter >= len(factors):
                r_col_boundary = self.img_size[0]
            else:
                r_col_boundary = int(min(r_col_boundary + (factors[factor_counter] * self.img_size[0]), self.img_size[0]))

        if self.mode == "convex":
            final_img.save(self.dir_name + "Slicer-convex-output" + self.img_ext)
        elif self.mode == "concave":
            final_img.save(self.dir_name + "Slicer-concave-output" + self.img_ext)
        else:
            final_img.save(self.dir_name + "Slicer-curved-output" + self.img_ext)


    def getConvexFactors(self):
        if self.num_imgs < 3:
            print("ERROR:    Number of input images must be greater than 2")
            print("Good Bye")
            exit()
        if self.num_imgs % 2 == 0:
            factors = [self.curve_depth, self.curve_depth]
            num_iters = int((self.num_imgs - 2) / 2)
            factor_step = (self.curve_depth - 1) / num_iters
        else:
            factors = [self.curve_depth]
            num_iters = int((self.num_imgs - 1) / 2)
            factor_step = (self.curve_depth - 1) / num_iters

        last_val = self.curve_depth
        for i in range(num_iters):
            factors.append(last_val - factor_step)
            factors.insert(0, last_val - factor_step)
            last_val = last_val - factor_step

        factor_sum = sum(factors)
        factors = [x / factor_sum for x in factors]

        return factors




    def getConcaveFactors(self):
        if self.num_imgs < 3:
            print("ERROR:    Number of input images must be greater than 2")
            print("Good Bye")
            exit()
        if self.num_imgs % 2 == 0:
            factors = [1, 1]
            num_iters = int((self.num_imgs - 2) / 2)
            factor_step = (self.curve_depth - 1) / num_iters
        else:
            factors = [1]
            num_iters = int((self.num_imgs - 1) / 2)
            factor_step = (self.curve_depth - 1) / num_iters

        last_val = 1
        for i in range(num_iters):
            factors.append(last_val + factor_step)
            factors.insert(0, last_val + factor_step)
            last_val = last_val + factor_step

        factor_sum = sum(factors)
        factors = [x / factor_sum for x in factors]

        return factors
