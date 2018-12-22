from slicer import Slicer

dir_name = "C:\\Users\\absch\\Desktop\\slicer-test\\"
img_ext = ".jpg"

slicer = Slicer(dir_name, img_ext, "simple", False)
slicer.slice()

convex_slicer = Slicer(dir_name, img_ext, "convex", False, 4)
convex_slicer.slice()

concave_slicer = Slicer(dir_name, img_ext, "concave", False, 4)
concave_slicer.slice()
