import numpy as np

class Arv360Frame:
    def __init__(self, other = None, width = -1, height = -1, bpp = 1 ):
        self.data = []
        self.width = width
        self.height = height
        self.projection = 0
        self.bytes_per_pixel = bpp

        if other is not None:
            self.data = other.data
            self.width = other.width
            self.height = other.height
            self.projection = other.projection
            self.bytes_per_pixel = other.bytes_per_pixel

    def rawData(self):
        array = bytearray()
        array.extend( self.data )
        return array

    def formatedData(self):
        array = bytearray()
        header = str(self.width) + 'x' + str(self.height) + '\n' + str(self.bytes_per_pixel) + '\n'
        array.extend(map(ord, header))
        array.extend( self.data )
        return array

    def cropFrame(self, x, y, w, h):
        crop_frame = Arv360Frame(width=w, height=h, bpp=self.bytes_per_pixel )
        np_frame = np.reshape( np.frombuffer( self.data ), (self.height,self.width))
        np_frame_crop = np.copy( np_frame[y:h,x:x+w] )
        crop_frame.data = np.getbuffer( np_frame_crop.flatten() )



