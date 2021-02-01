import numpy as np

class Arv360Frame:
    def __init__(self, other = None, width = -1, height = -1, bpp = 1 ):
        self.data = []
        self.width = width
        self.height = height
        self.projection = 0
        self.bytes_per_pixel = bpp
        self.layer = -1

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

        np_buffer = np.frombuffer( self.data, dtype = np.uint8 )

        bytes_Y = int( self.height * self.width )
        # Crop Y
        np_frame_Y = np.reshape( np_buffer[0:bytes_Y], (self.height,self.width))
        np_frame_Y_crop = np.copy( np_frame_Y[y:y+h,x:x+w] )

        uv_width = int( self.width / 2 )
        uv_height = int( self.height / 2 )
        x = int( x / 2 )
        y = int( y / 2 )
        w = int( w / 2 )
        h = int( h / 2 )
        bytes_UV = int( uv_height * uv_width )
        np_frame_U = np.reshape( np_buffer[bytes_Y:bytes_Y+bytes_UV], (uv_height,uv_width))
        np_frame_U_crop = np.copy( np_frame_U[y:y+h,x:x+w] )
        np_frame_V = np.reshape( np_buffer[bytes_Y+bytes_UV:bytes_Y+bytes_UV+bytes_UV], (uv_height,uv_width))
        np_frame_V_crop = np.copy( np_frame_V[y:y+h,x:x+w] )

        crop_frame.data = np.concatenate( (np_frame_Y_crop.flatten(), np_frame_U_crop.flatten(), np_frame_V_crop.flatten() ) ).tobytes()

        return crop_frame



