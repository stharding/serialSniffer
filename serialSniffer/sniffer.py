from serial import Serial
from concurrent.futures import ThreadPoolExecutor


class Sniffer(object):

    """
    TODO: write docstring
    """

    def __init__(self, virtual_comm='COM7', physical_comm='COM1'):
        self.virtual_comm = Serial(virtual_comm)
        self.physical_comm = Serial(physical_comm)
        self.pool = ThreadPoolExecutor(4)
        self.v_bytes = []
        self.p_bytes = []

        self.pool.submit(self.read_physical)
        self.pool.submit(self.read_virtual)

    def read_physical(self):

        """
        TODO: write docstring
        """

        while True:
            n = self.physical_comm.inWaiting()
            if n:
                msg = self.physical_comm.read()
                self.virtual_comm.write(msg)
                self.p_bytes.append(msg)
            # TODO: store the data somewhere

    def read_virtual(self):

        """
        TODO: write docstring
        """

        while True:
            n = self.virtual_comm.inWaiting()
            if n:
                msg = self.virtual_comm.read()
                self.physical_comm.write(msg)
                self.v_bytes.append(msg)
