import os
import subprocess
import tempfile

from .arvfifo import ArvFifo
from .arv360stream import Arv360StreamInput, Arv360StreamOutput
from .arvhandleconfig import ReadConfiguration, WriteConfigurationFile, FindLine, FindLineRegEx


Command360Convert = "360ConvertApp"
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
    [0, "ERP",  "Equi-rectangular projection", "1 1   0 0"],
    [1, "CMP",  "Cube-map projection",         "2 3   4 0 0 0 5 0   3 180 1 270 2 0"],
    [3, "COHP", "Compact OHP",                 "4 2   2 270  3 90  6 90  7 270  0 270  1 90  4 90  5 270"],
    [5, "CISP", "Compat ISP",                  "4 5   0 180 2 180 4 0 6 180 8 0   1 180 3 180 5 180 7 180 9 180    11 0 13 0 15 0 17 0 19 0   10 180 12 0 14 180 16 0 18 0"]
]


def ConvertProjectionList():
    available_projections = []
    for i in range( len(Config360ConvertProjection) ):
        available_projections.append((Config360ConvertProjection[i][1], Config360ConvertProjection[i][2]))
    return available_projections


def ConvertProjectionNameToInt(projection="NA"):
    if projection == "NA":
        return -1
    for i in range( len(Config360ConvertProjection) ):
        if Config360ConvertProjection[i][1] == projection:
            return int(Config360ConvertProjection[i][0])
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

    def InitConversion(self, input_video, projection):

        self.is_running = False

        projection_config_type = projection
        if projection_config_type == -1:
            # Invalid projection
            return

        projection_config_fps = Config360ConvertProjection[projection_config_type][3]

        # Get default config of conversion function
        self.convert_config = ReadConfiguration(Default360ConvertConfig)
        self.convert_config.append(["InputFile", self.send_fifo_fname])
        self.convert_config.append(["SourceWidth", input_video.width])
        self.convert_config.append(["SourceHeight", input_video.height])
        self.convert_config.append(["OutputFile", self.receive_fifo_fname])

        self.convert_config.append(["CodingGeometryType", projection_config_type])
        self.convert_config.append(["CodingFPStructure", projection_config_fps])

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
                # Problems here
                found = True
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
        self.send_stream.name = self.send_fifo_fname

        # Create stream to receive data from FIFO
        self.receive_stream = Arv360StreamInput()
        self.receive_stream.name = self.receive_fifo_fname
        self.receive_stream.width = converted_width
        self.receive_stream.height = converted_height
        self.receive_stream.bytes_per_pixel = 1
        self.receive_stream.PrintInfo()

        self.convert_to_projection = projection

        self.LaunchConvertCommand()

    def FinishConversion(self):
        if self.is_running:
            self.receive_stream.CloseStream()
            self.send_stream.CloseStream()

    def LaunchConvertCommand(self):
        if not self.is_running:
            command_to_run = [Command360Convert]
            command_to_run.extend(["-c", self.convert_config_fname])
            p = subprocess.Popen(command_to_run)
            self.send_stream.OpenStream()
            self.receive_stream.OpenStream()
            self.is_running = True

    def ConvertFrame(self, frame):
        self.LaunchConvertCommand()
        self.send_stream.WriteFrame(frame)
        return self.receive_stream.ReadFrame()
