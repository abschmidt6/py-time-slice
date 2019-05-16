import subprocess
from os import listdir, path
from PIL import Image
from myexceptions import *
class ImageProperties:
    def __init__(self, path, ext):
        """ Initialize Image Properties """
        self.path = path
        self.extension = ext
        self.mode = ""
        self.size = (0, 0)


class Slicer:

    def __init__(self, in_dir, out_dir, img_ext, mode, reverse = False, curve_depth = 1, num_slices = 0):
        """ Initialize Slicer. """
        self.slice_mode = mode      # simple, concave, convex
        self.num_imgs = 0
        self.num_slices = num_slices
        self.reverse = reverse      # True or False
        self.img_names = []         # list of image filenames
        self.col_width = 0          # Column width for simple mode
        self.curve_depth = curve_depth  # Curve depth for concave/convex modes
        self.out_dir = out_dir
        self.props = ImageProperties(in_dir, img_ext)

        self.curr_slice = None
        self.slice_iter = 0

        self.curr_exception = NoError("Nothing is wrong")

    def getImageNames(self):
        """ Get Image names from the provided input directory """
        # get all files within the dir_name directory
        try:
            output = listdir(self.props.path)
        except OSError:
            self.curr_exception = InternalError("OSError when listing files in:\n{}".format((self.props.path)))
            exit()

        # Append all filenames to a list
        # if they contain the img extension and don't contain "slicer"
        self.img_names = [ elem for elem in output if (self.props.extension in elem.lower() and "slicer" not in elem.lower())]
        self.img_names.sort()
        self.num_imgs = len(self.img_names)

        if self.num_imgs < 3:
            self.curr_exception = TooFewImagesError()
            exit()

        # Prune (temp)
        if self.num_slices > self.num_imgs:
            self.curr_exception = TooManySlicesError()
            exit()

        elif self.num_slices < self.num_imgs:
            self.pruneImages()



    def pruneImages(self):
        """ Reduce the image names list down to the number of slices """
        tmp_list = self.img_names
        self.img_names = list()
        factor = self.num_imgs / self.num_slices
        for i in range(self.num_slices):
            self.img_names.append(tmp_list[int(i * factor)])
        self.num_imgs = len(self.img_names)

    def slice(self):
        """ Perform the slice; create one images from many """
        self.getImageNames()
        self.getImageModeAndSize()

        if self.num_slices > self.props.size[0]:
            self.num_slices = self.props.size[0]

        if self.reverse:
            self.img_names.sort(reverse = True)

        if self.slice_mode == "linear":
            self.simpleSlice()
        elif self.slice_mode == "convex":
            self.warpedSlice(self.getConvexFactors())
        elif self.slice_mode == "concave":
            self.warpedSlice(self.getConcaveFactors())
        else:
            self.curr_exception = InternalError("Invalid mode")
            exit()

    def getImageModeAndSize(self):
        """ Get the image properties given a list of image names """
        try:
            img  = Image.open(path.join(self.props.path, self.img_names[0]))
        except IOError:
            self.curr_exception = ImageError(self.img_names[0])
            exit()

        self.props.mode = img.mode
        self.props.size = img.size

    def simpleSlice(self):
        """ Simplest slicing method, each slice has equal weight"""
        col_width =  [int(self.props.size[0] / self.num_imgs)] * self.num_imgs
        for i in range(int((self.props.size[0] % self.num_imgs) / 2)):
            col_width[i] += 1
            col_width[len(col_width) - 1 - i] += 1

        self.final_img = Image.new(self.props.mode, self.props.size)
        l_col_boundary = 0
        r_col_boundary = col_width[0]
        counter = 0
        for img_name in self.img_names:
            # Make sure image can open
            try:
                img  = Image.open(path.join(self.props.path, img_name))
            except IOError:
                self.curr_exception = ImageError(img_name)
                exit()

            self.curr_slice = img_name
            self.slice_iter += 1

            box = (l_col_boundary, 0, r_col_boundary, self.props.size[1])
            slice = img.crop(box)

            self.final_img.paste(slice, box)

            l_col_boundary = r_col_boundary
            r_col_boundary = min(r_col_boundary + col_width[counter], self.props.size[0])

        self.saveImage()

    def warpedSlice(self, factors=[]):
        """ Complex slice, where each slice has a different width """
        if len(factors) == 0:
            self.curr_exception = InternalError("Factors could not be obtained")
            exit()

        self.final_img = Image.new(self.props.mode, self.props.size)
        l_col_boundary = 0
        r_col_boundary = int(factors[0] * self.props.size[0])
        factor_counter = 0
        for img_name in self.img_names:
            # Make sure image can open
            factor_counter += 1
            try:
                img  = Image.open(path.join(self.props.path, img_name))
            except IOError:
                self.curr_exception = ImageError(img_name)
                exit()

            self.curr_slice = img_name
            self.slice_iter += 1

            box = (l_col_boundary, 0, r_col_boundary, self.props.size[1])
            slice = img.crop(box)

            self.final_img.paste(slice, box)

            l_col_boundary = r_col_boundary
            if factor_counter >= len(factors) - 1:
                r_col_boundary = self.props.size[0]
            else:
                r_col_boundary = int(min(r_col_boundary + (factors[factor_counter] * self.props.size[0]), self.props.size[0]))

        self.saveImage()


    def getConvexFactors(self):
        """ Return a list of factors used for a complex (Convex) slice """
        if self.num_imgs < 3:
            self.curr_exception = TooFewImagesError()
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
        """ Return a list of factors used for a complex (Concave) slice """
        if self.num_imgs < 3:
            self.curr_exception = TooFewImagesError()
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

    def saveImage(self):
        """ Saves the final img to the output directory """
        files = listdir(self.out_dir)
        filename = "slicer-{}-output".format(self.slice_mode)

        counter = 1
        while filename + self.props.extension in files:
            filename = "slicer-" + self.slice_mode + "-output" + str(counter)
            counter += 1

        fullname = path.join(self.out_dir, filename + self.props.extension)
        self.final_img.save(fullname)

    def getThreadUpdateInfo(self):
        """ Return progress of the slicer, for use with the GUI """
        return (self.curr_slice, self.slice_iter)