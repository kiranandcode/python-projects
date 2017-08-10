import ctypes
from ctypes import CDLL


class example:
    def __init__(self, favorite):
        self.example_class = CDLL('./example.dll')
        self.example_class .new_example_class.argtypes = [ctypes.c_double]
        self.example_class.new_example_class.restype  = ctypes.c_void_p


        self.example_class.example_add.argtypes = [ctypes.c_void_p,\
                ctypes.c_double, ctypes.c_double]
        self.example_class.example_add.restype = ctypes.c_double

        self.obj = self.example_class.new_example_class(favorite)


    def Add(self, a,b):
        return self.example_class.example_add(self.obj, a,b)

    def delete():
        return self.example_class.del_example_class(self.obj)

