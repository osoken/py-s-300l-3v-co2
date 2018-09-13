# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread

import serial


class S300L3VSensor(Thread):
    def __init__(self, dev, baudrate=38400, timeout=10.0, hook=None):
        super(S300L3VSensor, self).__init__()
        self.serial = serial.Serial(
            dev, baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout
        )
        self.__renew()
        self.__hook = hook if hook is not None else lambda v: None
        self.start()

    def __renew(self):
        s = self.serial.read(12)
        s = s.decode('utf-8')
        offset = s.index('\n') + 1
        s = s[offset:] + s[:offset]
        val = int(s[:6])
        self.__latest_value = val

    def run(self):
        while True:
            self.__renew()
            self.__hook(dict(zip(self.attributes(), self.values())))
            sleep(1)

    def attributes(self):
        return ('co2', )

    def values(self):
        return (self.co2, )

    @property
    def co2(self):
        retrn self.__latest_value

    def __getitem__(self, attr):
        if attr in self.attributes():
            return getattr(self, attr)
        raise KeyError(attr)
