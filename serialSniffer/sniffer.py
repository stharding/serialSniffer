from serial import Serial
from time import time
from concurrent.futures import ThreadPoolExecutor


class Message(object):
    def __init__(self, src, dst, data, time_stamp=None):
        self.src  =  src
        self.dst  =  dst
        self.data =  data
        self.time_stamp = time_stamp
        if time_stamp is None:
            self.time_stamp = time()

    def __repr__(self):
        return 'Message(' + ', '.join([self.src, self.dst, self.data, str(self.time_stamp)]) + ')'


class Sniffer(object):

    """
    TODO: write docstring
    """

    def __init__(self, virtual_comm='COM7', physical_comm='COM1'):
        self.virtual_comm = Serial(virtual_comm, baudrate=19200)
        self.physical_comm = Serial(physical_comm, baudrate=19200)
        self.pool = ThreadPoolExecutor(4)
        self.messages = []

        self.pool.submit(self.read_physical)
        self.pool.submit(self.read_virtual)

    def read_physical(self):

        """
        TODO: write docstring
        """

        while True:
            msg = self.physical_comm.read()
            n = self.physical_comm.inWaiting()
            if n:
                msg += self.physical_comm.read(n)
            # print 'wrote', self.virtual_comm.write(msg), 'bytes to COM7'
            self.virtual_comm.write(msg)
            self.messages.append(Message(self.physical_comm.port, self.virtual_comm.port, msg))
            # TODO: store the data somewhere

    def read_virtual(self):

        """
        TODO: write docstring
        """

        while True:
            msg = self.virtual_comm.read()
            n = self.virtual_comm.inWaiting()
            if n:
                msg += self.virtual_comm.read(n)
            self.physical_comm.write(msg)
            self.messages.append(Message(self.virtual_comm.port, self.physical_comm.port, msg))

