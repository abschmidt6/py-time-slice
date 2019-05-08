from slicer import Slicer

#dir_name = "C:\\Users\\absch\\Desktop\\Slicer-test\\"
dir_name = "/mnt/c/Users/absch/Desktop/Slicer-test/"
img_ext = ".jpg"

slicer = Slicer(dir_name, img_ext, "simple", reverse = False, num_slices = 20)
slicer.slice()

# convex_slicer = Slicer(dir_name, img_ext, "convex", False, 10)
# convex_slicer.slice()
#
# concave_slicer = Slicer(dir_name, img_ext, "concave", False, 10)
# concave_slicer.slice()
