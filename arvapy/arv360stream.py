class Arv360Stream:
    def __init__(self, other=None):
        self.binary_file = None
        self.name = None
        self.width = -1
        self.height = -1
        self.frame_rate = -1
        self.projection = 0
        self.bytes_per_pixel = 1
        self.num_layers = 1

        if other is not None:
            self.name = other.name
            self.width = other.width
            self.height = other.height
            self.frame_rate = other.frame_rate
            self.projection = other.projection
            self.bytes_per_pixel = other.bytes_per_pixel
            self.num_layers = other.num_layers

    def CloseStream(self):
        self.binary_file.close()

    def PrintInfo(self):
        print("Stream Name:   " + self.name)
        print("       Width:  " + str(self.width))
        print("       Height: " + str(self.height))
        print("       Bpp:    " + str(self.bytes_per_pixel))
        print("       Layers: " + str(self.num_layers))


class Arv360StreamInput(Arv360Stream):
    def __init__(self, other=None):
        Arv360Stream.__init__(self, other)

    def OpenStream(self):
        self.binary_file = open(self.name, "rb")

    def ReadFrame(self):
        frame_size = self.width * self.height * self.bytes_per_pixel * 1.5
        frame = self.binary_file.read(int(frame_size))
        return frame


class Arv360StreamOutput(Arv360Stream):
    def __init__(self, other=None):
        Arv360Stream.__init__(self, other)

    def OpenStream(self):
        self.binary_file = open(self.name, "wb")

    def WriteFrame(self, frame):
        self.binary_file.write(frame)
