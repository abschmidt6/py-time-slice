from slicer import Slicer
import time
import datetime

dir_name = "C:\\Users\\absch\\Desktop\\slicer-test-large\\"
img_ext = ".jpg"

test_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
f = open("timelog.txt", "a")

begin = time.clock()
slicer = Slicer(dir_name, img_ext, "simple", False)
slicer.slice()
f.write(test_timestamp + "\t\tSimple\t\t" + str(round(time.clock() - begin, 4)) + "\n")

begin = time.clock()
convex_slicer = Slicer(dir_name, img_ext, "convex", False, 10)
convex_slicer.slice()
f.write(test_timestamp + "\t\tConvex\t\t" + str(round(time.clock() - begin, 4)) + "\n")

begin = time.clock()
concave_slicer = Slicer(dir_name, img_ext, "concave", False, 10)
concave_slicer.slice()
f.write(test_timestamp + "\t\tConcave\t\t" + str(round(time.clock() - begin, 4)) + "\n")
