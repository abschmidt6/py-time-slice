from slicer import Slicer

dir_name = "C:\\Users\\absch\\Desktop\\slicer-test-large\\"
img_ext = ".jpg"

slicer = Slicer(dir_name, img_ext, "simple", False)
slicer.slice()

convex_slicer = Slicer(dir_name, img_ext, "convex", False, 10)
convex_slicer.slice()

concave_slicer = Slicer(dir_name, img_ext, "concave", False, 10)
concave_slicer.slice()
