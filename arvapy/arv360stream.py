class Arv360Stream:
    def __init__(self, other=None):
        self.binary_file = []
        self.name = None
        self.filename = None
        self.filename_list = None
        self.width = -1
        self.height = -1
        self.resolution_list = None
        self.frame_rate = -1
        self.projection = 0
        self.bytes_per_pixel = 1
        self.num_layers = 1

        if other is not None:
            self.name = other.name
            self.filename = other.filename
            self.filename_list = other.filename_list
            self.width = other.width
            self.height = other.height
            self.resolution_list = other.resolution_list
            self.frame_rate = other.frame_rate
            self.projection = other.projection
            self.bytes_per_pixel = other.bytes_per_pixel
            self.num_layers = other.num_layers

        self.width = self.GetWidth()
        self.height = self.GetHeight()

    def CloseStream(self):
        for file in self.binary_file:
            file.close()

    def GetFileName(self, layer = -1 ):
        if self.num_layers > 1:
            layer = self.num_layers -1 if layer == -1 else layer
            return self.filename_list[layer]
        return self.filename

    def GetWidth(self, layer = -1):
        if self.num_layers > 1:
            layer = self.num_layers -1 if layer == -1 else layer
            return self.resolution_list[layer][0]
        return self.width
        
    def GetHeight(self, layer = -1):
        if self.num_layers > 1:
            layer = self.num_layers -1 if layer == -1 else layer
            return self.resolution_list[layer][1]
        return self.height

    def PrintInfo(self):
        if self.name is None:
            name = self.filename
        else:
            name = self.name
        if self.filename_list is None:
            filename = self.filename
        else:
            filename = self.filename_list
        print("Stream Name: " + name)
        print("   Filename: " + str(filename))
        print("      Width: " + str(self.width))
        print("     Height: " + str(self.height))
        print("        Bpp: " + str(self.bytes_per_pixel))
        print("     Layers: " + str(self.num_layers))


class Arv360StreamInput(Arv360Stream):
    def __init__(self, other=None):
        Arv360Stream.__init__(self, other)

    def OpenStream(self):
        if self.filename_list is not None:
            for file in self.filename_list:
                self.binary_file.append( open(file, "rb") )
        else:
            self.binary_file.append( open(self.filename, "rb") )
        

    def ReadFrame(self, layer = -1):
        if layer == -1:
            layer = self.num_layers - 1
        frame_size = self.GetWidth(layer) * self.GetHeight(layer) * self.bytes_per_pixel * 1.5
        frame = self.binary_file[layer].read(int(frame_size))
        return frame


class Arv360StreamOutput(Arv360Stream):
    def __init__(self, other=None):
        Arv360Stream.__init__(self, other)

    # def OpenStream(self):
    #     if self.filename_list is not None:
    #         for file in self.filename_list:
    #             self.binary_file.append( open(file, "wb") )
    #     else:
    #         self.binary_file.append( open(self.filename, "wb") )

    def OpenStream(self):
        self.binary_file.append( open(self.filename, "wb") )

    def WriteFrame(self, frame, layer = -1):
        if layer == -1:
            layer = self.num_layers - 1
        self.binary_file[layer].write(frame)
