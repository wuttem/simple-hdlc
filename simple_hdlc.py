#!/usr/bin/python
# coding: utf8

__version__ = '0.1'

import logging
import struct
import time
from PyCRC.CRCCCITT import CRCCCITT


def calcCRC(data):
    logging.error(data)
    crc = CRCCCITT("FFFF").calculate(bytes(data))
    logging.error(crc)
    b = bytearray(struct.pack("<H", crc))
    return b

class Frame(object):
    STATE_READ = 0x01
    STATE_ESCAPE = 0x02

    def __init__(self):
        self.finished = False
        self.error = False
        self.state = self.STATE_READ
        self.data = bytearray()
        self.crc = bytearray()

    def __len__(self):
        return len(self.data)

    def addByte(self, b):
        if b == 0x7D:
            self.state = self.STATE_ESCAPE
        elif self.state == self.STATE_ESCAPE:
            self.state = self.STATE_READ
            b = b ^ 0x20
            self.data.append(b)
        else:
            self.data.append(b)

    def finish(self):
        self.crc = self.data[-2:]
        self.data = self.data[:-2]
        self.finished = True

    def checkCRC(self):
        logging.error("check crc %s - %s", self.crc, calcCRC(self.data))
        res = bool(self.crc == calcCRC(self.data))
        if not res:
            self.error = True
        return res

    def toString(self):
        return str(self.data)


class HDLC(object):
    def __init__(self, serial):
        self.serial = serial
        self.current_frame = None

    @classmethod
    def toBytes(cls, data):
        return bytearray(data)

    def sendFrame(self, data):
        bs = self._encode(self.toBytes(data))
        self.serial.write(bs)

    def readFrame(self, timeout=5):
        timer = time.time() + timeout
        while time.time() < timer:
            i = self.serial.in_waiting
            if i < 1:
                time.sleep(0.0001)
                continue

            new_byte = ord(self.serial.read(1))
            if new_byte == 0x7E:
                # Start or End
                if not self.current_frame or len(self.current_frame) < 1:
                    # Start
                    self.current_frame = Frame()
                else:
                    self.current_frame.finish()
                    self.current_frame.checkCRC()
            else:
                self.current_frame.addByte(new_byte)

            # Validate and return
            if self.current_frame.finished and not self.current_frame.error:
                # Success
                s = self.current_frame.toString()
                self.current_frame = None
                return s
            elif self.current_frame.finished:
                # Error
                self.current_frame = None
                raise ValueError("Invalid Frame (CRC FAIL)")
        raise RuntimeError("readFrame timeout")

    @classmethod
    def _encode(cls, bs):
        data = bytearray()
        data.append(0x7E)
        crc = calcCRC(bs)
        for byte in bs:
            if byte == 0x7E or byte == 0x7D:
                data.append(0x7D)
                data.append(byte ^ 0x20)
            else:
                data.append(byte)
        data += crc
        data.append(0x7E)
        return bytes(data)
