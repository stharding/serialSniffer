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
            p_byte = self.virtual_comm.read()
            self.virtual_comm.write(p_byte)
            self.p_bytes.append(p_byte)
            # TOCO: store the data somewhere

    def read_virtual(self):

        """
        TODO: write docstring
        """

        while True:
            v_byte = self.virtual_comm.read()
            self.physical_comm.write(v_byte)
            self.v_bytes.append(v_byte)
