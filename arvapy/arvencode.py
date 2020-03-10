import tempfile
import subprocess

from pathlib import Path
from os.path import expanduser  # This is needed to swap "~" for $HOME in strings


class ArvApyEncode:
    def __init__(self, encoder_path):
        """
        Initialises an object of the calsse ArvApyEncode

        This constructor initializes an object of the
        ArvApyEncode Class, responsible for preparing
        the configurations of the encoding process and
        launch it.

        Parameters
        ----------
        encoder_path : str
            Path for the encoder executable
        arg2 : str
            Description of arg2

        Returns
        -------
        ArvApyEncode
            ArvApyEncode object

        """
        # DEBUG -- PATH MUST BY DYNAMICALLY SET
        self.cfg_search_path = "~/Repos/vtm_360lib"

        # Encoding parameters
        self.encoder_path  = encoder_path
        self.qps           = []    # List of QPs (if more than one is set, a command for each QP is generated)
        self.frames_to_enc = 0     # Numer of frames from the sequence to be encoded
        self.orig_yuv_path = ""    # Path of the sequence to be encoded
        self.rec_yuv_path  = ""    # Path where the reconstructed yuv sequence will be stored
        self.out_bin_path  = ""    # Path where the encoded binary sequqnce will be stored
        self.dtrace_rule   = ""    # DTRACE_RULE (rule that sets wich statistics are stored, if any)
        self.dtrace_path   = ""    # Path where the statitics defined by the trace rule will be stored
        self.cfg_files     = []

        # Encoding commands
        self.enc_cmd       = []    # Array where all the encogind commands are saved (there should be 1 per qp)

    def GetAvailableConfigFiles(self):
        """
        Returns list of configuration files

        This function returns a list with the paths for
        all configuration (*.cfg) files found in the
        search path.

        Returns
        -------
        list
            list of paths to cfg files

        """
        # Check if the encoding command as already been generated

        cfg_files = [path for path in Path(expanduser(self.cfg_search_path)).rglob("*.cfg")]
        return cfg_files

    def SetCodingParameters(self, orig_yuv_path, rec_yuv_path, out_bin_path, cfg_files, qp=[22], frames_to_enc=0, dtrace_rule="", dtrace_path=""):
        '''Sets the coding parameters as object fields, previously initialised by the constructor'''
        self.orig_yuv_path = orig_yuv_path
        self.rec_yuv_path  = rec_yuv_path
        self.out_bin_path  = out_bin_path
        self.cfg_files     = cfg_files
        self.qps           = qp
        self.frames_to_enc = frames_to_enc
        self.dtrace_rule   = dtrace_rule
        self.dtrace_path   = dtrace_path

    def GenEncodingCommand(self):
        '''Generates the command that is lauched to encode a given image, with respective parameters'''
        # Check if minimal parameters for the encoding process are set. If not, exception is raised
        if not self.qps or not self.orig_yuv_path or not self.rec_yuv_path or not self.out_bin_path or not self.cfg_files:
            raise NameError("Invalid encoding arguments. Please run SetCodingParameters method first.")

        for qp in self.qps:
            cmd = []

            # Include path to encoder in the command
            cmd.append(self.encoder_path)

            # Set all config files selected. It is expected that a file tailor made for the sequence is given
            for cfg in self.cfg_files:
                cmd.append("-c")
                cmd.append(cfg)

            # Set QP
            cmd.append("-q")
            cmd.append(str(qp))

            # Set Number of frames to be encoded, if set
            if self.frames_to_enc < 1:
                cmd.append("-f")
                cmd.append(str(self.frames_to_enc))

            # Set input file path
            cmd.append("-i")
            cmd.append(self.orig_yuv_path)

            # Set reconstructed output sequence path
            cmd.append("-o")
            cmd.append(self.rec_yuv_path)

            # Set output binary encoded file
            cmd.append("-b")
            cmd.append(self.out_bin_path)

            # Set trace rules and trace file path, if sets
            if self.dtrace_path and self.dtrace_rule:
                cmd.append("--TraceFile")
                cmd.append(self.dtrace_path)

                cmd.append("--TraceRule")
                cmd.append(self.dtrace_rule)

            # Save command in the enc_cmd list
            self.enc_cmd.append(cmd)

    def PrintEncodigCommand(self):
        """
        Prints the encoding commands

        This function provides an overview of the commands that were built and
        are going to be run with the method EncodeSequence.
        """
        # Check if the encoding command as already been generated
        if not self.enc_cmd:
            raise NameError("Invalid encoding command. Please run GenEncodingCommand method first.")

        for cmd in self.enc_cmd:
            print(" ".join(cmd))

    # TODO test this method!
    def EncodeSequence(self):
        log_file = tempfile.NamedTemporaryFile(mode="w", prefix="arvapy_360_encode_log_").name
        with open(log_file, "a") as output_file:
            # Spawn an encoding process for every QP. Processes are launch sequentially
            for cmd in self.enc:
                p = subprocess.call(cmd, stdout=output_file, stderr=output_file)


# FOR SELF CONTAINED DEBUG ONLY!! TO BE ERASED IN FINAL VERSION
if __name__ == "__main__":
    encode_proc = ArvApyEncode("path_to_vvc/EncApp")

    # print(encode_proc.cfg_search_path)
    # print(encode_proc.GetAvailableConfigFiles())

    encode_proc.SetCodingParameters("orig_path.yuv","rec_path.yuv","out_path.bin",["1.cfg","2.cfg","3.cfg"],[22,27,32,37],frames_to_enc=1)
    encode_proc.GenEncodingCommand()
    encode_proc.PrintEncodigCommand()
