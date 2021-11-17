from .arvutils import readSummaryFile

from math import floor
from os import path
class Arv360Stream:
    def __init__(self, other=None):
        self.binary_file = []
        self.name = None
        self.filename = None
        self.filename_list = None
        self.width = -1
        self.height = -1
        self.resolution_list = None
        self.quality_list = None
        self.frame_rate = -1
        self.projection = 0
        self.bytes_per_pixel = 1
        self.num_layers = 1
        self.summary_info_file = ""
        self.summary_info = []
        self.average_bitrate = 9999

        if other is not None:
            self.name = other.name
            self.filename = other.filename
            self.filename_list = other.filename_list
            self.width = other.width
            self.height = other.height
            self.resolution_list = other.resolution_list
            self.quality_list = other.quality_list
            self.frame_rate = other.frame_rate
            self.projection = other.projection
            self.bytes_per_pixel = other.bytes_per_pixel
            self.num_layers = other.num_layers
            self.summary_info_file = other.summary_info_file
            # We do not need to copy summary_info since we can just read from file on Open
            self.average_bitrate = other.average_bitrate

        if self.num_layers > 1:
            assert( len( self.filename_list ) == self.num_layers )
            assert( len( self.resolution_list ) == self.num_layers )
            assert( len( self.quality_list ) == self.num_layers )

        self.width = self.GetWidth()
        self.height = self.GetHeight()

        self.num_of_ctus_width = floor( self.width + 127 / 128 )
        self.num_of_ctus_height = floor( self.height + 127 / 128 )

    def LayerInformation(self):
        layer_info = []
        try:
            for l in range( self.num_layers):
                l_info = "Quality: %s | Resolution: %dx%d" % (self.quality_list[l], self.resolution_list[l][0], self.resolution_list[l][1] )
                layer_info.append( (l, l_info) )
        except:
            l_info = "Quality: %s | Resolution: %dx%d" % (0, self.width, self.height )
            layer_info.append( (0, l_info) )
        return layer_info

    def ReadSummaryInfo(self):
        if path.exists(self.summary_info_file):
            self.summary_info = readSummaryFile( self.summary_info_file )

    def CloseStream(self):
        for file in self.binary_file:
            file.close()

    def GetFileName(self, layer = -1 ):
        if self.num_layers > 1:
            layer = self.num_layers -1 if layer == -1 else layer
            return self.filename_list[layer]
        return self.filename

    def GetDimensionSize(self, layer, dim):
        if self.resolution_list is not None and len(self.resolution_list) > layer and layer < self.num_layers:
            layer = self.num_layers -1 if layer == -1 else layer
            return self.resolution_list[layer][dim]
        return -1

    def GetWidth(self, layer = -1):
        width = self.GetDimensionSize(layer, 0 )
        return width if width > 0 else self.width

    def GetHeight(self, layer = -1):
        height = self.GetDimensionSize(layer, 1 )
        return height if height > 0 else self.height

    def GetBitrate(self, layer = -1 ):
        try:
            return float( self.summary_info["Bitrate_L0"] )
        except:
            pass
        return self.average_bitrate

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

        self.ReadSummaryInfo()


    def ReadFrame(self, layer = -1):
        if layer == -1:
            layer = self.num_layers - 1
        frame_size = self.GetWidth(layer) * self.GetHeight(layer) * self.bytes_per_pixel * 1.5
        frame = self.binary_file[layer].read(int(frame_size))
        if frame is None or len(frame) != frame_size:
            self.binary_file[layer].seek(0)
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
