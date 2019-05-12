# py-time-slice
## A python program written to create timeslice images

There are currently 3 working modes:  
--   Linear:    Linear slice, all images have equal weight  
--   Convex:    Variable slice, images in center have more weight  
--   Concave:   Variable slice, images on edges have more weight  

Additionally, all three modes can be run in reverse, to swap the ordering of the images  

Simple:  
![alt text](https://github.com/abschmidt6/py-time-slice/blob/master/Slicer-simple-output.jpg "Simple Slice")  

Convex:  
![alt text](https://github.com/abschmidt6/py-time-slice/blob/master/Slicer-convex-output.jpg "Convex Slice")  

Concave:  
![alt text](https://github.com/abschmidt6/py-time-slice/blob/master/Slicer-concave-output.jpg "Concave Slice")  


## TODO
--  Optimize(!!!)  
--  Fix concave/convex factors  
--  Remove Black Bars from concave and convex modes

## GUI TODO
--  Fix threads (they should end when GUI is closed)
--  Reduce number of member variables where possible
