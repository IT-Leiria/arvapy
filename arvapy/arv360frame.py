class Arv360Frame:
    def __init__(self, other=None):
        self.data = []
        self.width = -1
        self.height = -1
        self.projection = 0
        self.bytes_per_pixel = 1

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



