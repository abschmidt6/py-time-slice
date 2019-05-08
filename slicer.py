import subprocess
from PIL import Image
class ImageProperties:
    def __init__(self, path, ext):
        self.path = path
        self.extension = ext
        self.mode = ""
        self.size = (0, 0)


class Slicer:

    def __init__(self, dir_name, img_ext, mode, reverse = False, curve_depth = 1, num_slices = 0):
        self.slice_mode = mode      # simple, concave, convex
        self.num_imgs = 0
        self.num_slices = num_slices
        self.reverse = reverse      # True or False
        self.img_names = []         # list of image filenames
        self.col_width = 0          # Column width for simple mode
        self.curve_depth = curve_depth  # Curve depth for concave/convex modes
        self.props = ImageProperties(dir_name, img_ext)

    def getImageNames(self):
        # get all files within the dir_name directory
        output = subprocess.check_output(["dir", self.props.path])

        # Append all filenames to a list
        # if they contain the img extension and don't contain "slicer"
        self.img_names = [ elem for elem in output.decode().split() if (self.props.extension in elem.lower() and "slicer" not in elem.lower())]
        self.img_names.sort()
        self.num_imgs = len(self.img_names)

        if self.num_imgs < 3:
            print("ERROR::   Image names could not be selected from {}".format((self.props.path)))
            print("Number of images selected = {}".format((self.num_imgs)))
            print("Expected 3+ images, found fewer ... exiting")
            exit()

        # Prune (temp)
        if self.num_slices > self.num_imgs:
            print("ERROR::   Too many slices")
            print("Number of slices must be < Number of images ... exiting")
            exit()

        elif self.num_slices < self.num_imgs:
            self.pruneImages()


    def pruneImages(self):
        tmp_list = self.img_names
        self.img_names = list()
        factor = self.num_imgs / self.num_slices
        for i in range(self.num_slices):
            self.img_names.append(tmp_list[int(i * factor)])
        self.num_imgs = len(self.img_names)

    def slice(self):
        self.getImageNames()
        self.getImageModeAndSize()

        if self.reverse:
            self.img_names.sort(reverse = True)

        if self.slice_mode == "simple":
            self.simpleSlice()
        elif self.slice_mode == "convex":
            self.warpedSlice(self.getConvexFactors())
        elif self.slice_mode == "concave":
            self.warpedSlice(self.getConcaveFactors())
        else:
            print("ERROR::    Invalid Mode")
            print("Good Bye")
            exit()

    def getImageModeAndSize(self):
        img  = Image.open(self.props.path + self.img_names[0])
        self.props.mode = img.mode
        self.props.size = img.size

    def simpleSlice(self):
        col_width =  int(self.props.size[0] / self.num_imgs)

        final_img = Image.new(self.props.mode, self.props.size)
        l_col_boundary = 0
        r_col_boundary = col_width
        for img_name in self.img_names:
            # Make sure image can open
            try:
                img  = Image.open(self.props.path + img_name)
                print("Processing: " + str(img_name))
            except IOError:
                print("ERROR::   Image: " + img_name + " could not be opened")
                print("Good Bye")
                exit()

            for i in range(l_col_boundary, r_col_boundary):
                for j in range(self.props.size[1]):
                    final_img.putpixel((i,j), img.getpixel((i,j)))

            l_col_boundary = r_col_boundary
            r_col_boundary = min(r_col_boundary + col_width, self.props.size[0])

        final_img.save(self.props.path + "Slicer-simple-output" + self.props.extension)

    def warpedSlice(self, factors=[]):
        if len(factors) == 0:
            print("ERROR::    Factors could not be obtained")
            print("Good Bye")
            exit()

        final_img = Image.new(self.props.mode, self.props.size)
        l_col_boundary = 0
        r_col_boundary = int(factors[0] * self.props.size[0])
        factor_counter = 0
        for img_name in self.img_names:
            # Make sure image can open
            factor_counter += 1
            try:
                img  = Image.open(self.props.path + img_name)
                print("Processing: " + str(img_name))
            except IOError:
                print("ERROR::   Image: " + img_name + " could not be opened")
                print("Good Bye")
                exit()

            for i in range(l_col_boundary, r_col_boundary):
                for j in range(self.props.size[1]):
                    final_img.putpixel((i,j), img.getpixel((i,j)))

            l_col_boundary = r_col_boundary
            if factor_counter >= len(factors):
                r_col_boundary = self.props.size[0]
            else:
                r_col_boundary = int(min(r_col_boundary + (factors[factor_counter] * self.props.size[0]), self.props.size[0]))

        if self.mode == "convex":
            final_img.save(self.props.path + "Slicer-convex-output" + self.props.extension)
        elif self.mode == "concave":
            final_img.save(self.props.path + "Slicer-concave-output" + self.props.extension)
        else:
            final_img.save(self.props.path + "Slicer-curved-output" + self.props.extension)


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
