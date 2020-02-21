import tempfile
import os


class ArvFifo:
    def __init__(self):
        self.send_fifo_fname = tempfile.NamedTemporaryFile(prefix="arvapy_fifo_send_").name
        self.receive_fifo_fname = tempfile.NamedTemporaryFile(prefix="arvapy_fifo_receive_").name

    def create_fifo(self):
        if not os.path.exists(self.send_fifo_fname):
            os.mkfifo(self.send_fifo_fname)
        if not os.path.exists(self.receive_fifo_fname):
            os.mkfifo(self.receive_fifo_fname)
        return True
