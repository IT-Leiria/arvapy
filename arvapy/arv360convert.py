import os
import subprocess
import tempfile

from .arvfifo import ArvFifo
from .arv360frame import Arv360Frame
from .arv360stream import Arv360StreamInput, Arv360StreamOutput
from .arvhandleconfig import ReadConfiguration, WriteConfigurationFile, FindLine, FindLineRegEx


Command360Convert = "/src/vtm/bin/360ConvertAppStatic"

Default360ConvertConfig = """InputGeometryType             : 0
                             SourceFPStructure             : 1 1   0 0 100
                             CodingGeometryType            : 1
                             CodingFPStructure             : 2 3   4 0 0 0 5 0   3 180 1 270 2 0
                             SVideoRotation                : 0 0  0
                             CodingFaceWidth               : 0
                             CodingFaceHeight              : 0
                             InterpolationMethodY          : 2
                             InterpolationMethodC          : 2
                             FaceSizeAlignment             : 1
                             InputBitDepth                 : 8
                             InternalBitDepth              : 8
                             OutputBitDepth                : 8
                             InputChromaFormat             : 420
                             FrameRate                     : 60
                             FrameSkip                     : 0
                             FramesToBeEncoded             : 999"""

Config360ConvertProjection = [
    ["ERP",  "Equi-rectangular projection", 0, "1 1   0 0"],
    ["CMP",  "Cube-map projection",         1, "2 3   4 0 0 0 5 0   3 180 1 270 2 0"],
    #["COHP", "Compact OHP",                 3, "4 2   2 270  3 90  6 90  7 270  0 270  1 90  4 90  5 270"],
    ["RECT", "Rectilinear projection",      4, "1 1   0 0"],
    ["CISP", "Compat ISP",                  5, "4 5   0 180 2 180 4 0 6 180 8 0   1 180 3 180 5 180 7 180 9 180    11 0 13 0 15 0 17 0 19 0   10 180 12 0 14 180 16 0 18 0"]
]


def ConvertProjectionList():
    available_projections = []
    for i in range( len(Config360ConvertProjection) ):
        if Config360ConvertProjection[i][2] == 4:
            continue
        available_projections.append((Config360ConvertProjection[i][0], Config360ConvertProjection[i][1]))
    return available_projections


def ConvertProjectionNameToInt(projection_name="NA"):
    if projection_name == "NA":
        return -1
    for i in range( len(Config360ConvertProjection) ):
        if Config360ConvertProjection[i][0] == projection_name:
            return i
    return -1


class Arv360Convert(ArvFifo):
    def __init__(self):
        ArvFifo.__init__(self)
        # Mark application as not running
        self.is_running = False
        self.convert_to_projection = -1
        self.convert_config = []
        self.convert_config_fname = ""
        self.send_stream = None
        self.receive_stream = None
        self.convertion_hash = 0

    def InitConversion(self, input_video, projection_idx, width = 0, height = 0, viewport_settings = [] ):

        self.is_running = False

        if projection_idx == -1 or projection_idx >= len( Config360ConvertProjection ):
            # Invalid projection
            raise "Invalid projection"

        projection_config_type = Config360ConvertProjection[projection_idx][2]
        projection_config_fps = Config360ConvertProjection[projection_idx][3]

        # Get default config of conversion function
        self.convert_config = ReadConfiguration(Default360ConvertConfig)
        self.convert_config.append(["InputFile", self.send_fifo_fname])
        self.convert_config.append(["SourceWidth", input_video.width])
        self.convert_config.append(["SourceHeight", input_video.height])
        self.convert_config.append(["OutputFile", self.receive_fifo_fname])
        self.convert_config.append(["CodingGeometryType", projection_config_type])
        self.convert_config.append(["CodingFPStructure", projection_config_fps])

        if width > 0:
          self.convert_config.append(["CodingFaceWidth", width])
        if height > 0:
          self.convert_config.append(["CodingFaceHeight", height])
        if viewport_settings:
          self.convert_config.append(["ViewPortSettings", viewport_settings])

        self.convert_config_fname = tempfile.NamedTemporaryFile(prefix="arvapy_360_convert_config_").name

        # Dry run to check the output file
        command_to_run = [Command360Convert]
        command_to_run.extend(["-c", self.convert_config_fname, "-i", "/dev/null"])
        WriteConfigurationFile(self.convert_config, self.convert_config_fname)

        log_file = tempfile.NamedTemporaryFile(mode='w', prefix="arvapy_360_convert_log_").name
        with open(log_file, 'a') as output_f:
            p = subprocess.call(command_to_run, stdout=output_f, stderr=output_f)

        line_found = FindLineRegEx(log_file, "Output * File *:")
        if line_found != -1:
            output_file = line_found.split(":")[1].strip()
            if not os.path.exists(output_file):
                raise "Could not find the output file in the conversion module"
                found = True
        else:
            raise "Could not find the output file in the conversion module"

        os.remove(output_file)

        # Guess packed resolution
        pack_res_line = FindLine(log_file, "Packed frame resolution:")
        pack_res = pack_res_line.split(' ')[3].split('x')
        converted_width = int(pack_res[0])
        converted_height = int(pack_res[1])

        self.receive_fifo_fname = output_file

        # Create FIFO
        self.create_fifo()

        # Create stream to send data to FIFO
        self.send_stream = Arv360StreamOutput(input_video)
        self.send_stream.filename = self.send_fifo_fname
        self.send_stream.num_layers = 1

        # Create stream to receive data from FIFO
        self.receive_stream = Arv360StreamInput()
        self.receive_stream.filename = self.receive_fifo_fname
        self.receive_stream.width = converted_width
        self.receive_stream.height = converted_height
        self.receive_stream.bytes_per_pixel = 1
        self.receive_stream.num_layers = 1
        self.receive_stream.PrintInfo()

        self.convert_to_projection = projection_idx

        self.LaunchConvertCommand()

    def FinishConversion(self):
        if self.is_running:
            self.receive_stream.CloseStream()
            self.send_stream.CloseStream()

        self.convert_to_projection = -1

    def LaunchConvertCommand(self):
        if not self.is_running:
            command_to_run = [Command360Convert]
            command_to_run.extend(["-c", self.convert_config_fname])
            p = subprocess.Popen(command_to_run)
            self.send_stream.OpenStream()
            self.receive_stream.OpenStream()
            self.is_running = True

    def ConvertFrame(self, input_frame):

        if input_frame.data is None or len(input_frame.data) == 0:
            return Arv360Frame(input_frame)

        output_frame = Arv360Frame(input_frame)
        output_frame.width = self.receive_stream.width
        output_frame.height = self.receive_stream.height
        output_frame.bytes_per_pixel = self.receive_stream.bytes_per_pixel
        output_frame.projection = self.convert_to_projection

        self.LaunchConvertCommand()
        self.send_stream.WriteFrame(input_frame.data)
        output_frame.data = self.receive_stream.ReadFrame()

        return output_frame
