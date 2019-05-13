class Error(Exception):
   """Base class for other exceptions"""
   pass

class NoError(Error):
    """Default error state when everything is fine

       Used for handling exceptions accross threads"""
    pass

class TooFewImagesError(Error):
   """Raised when the input value is too small"""
   pass

class TooManySlicesError(Error):
   """Raised when the input value is too large"""
   pass

class ImageError(Error):
    """Raised when an image cannot be opened"""
    def __init__(self, img):
        self.img = img

class InternalError(Error):
    def __init__(self, txt):
        self.txt = txt