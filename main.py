from slicer import Slicer

dir_name = "C:\\Users\\absch\\Desktop\\slicer-test\\"
img_ext = ".jpg"

slicer = Slicer(dir_name, img_ext, "simple")
slicer.slice()
