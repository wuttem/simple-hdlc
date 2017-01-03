#!/usr/bin/python
# coding: utf8

import unittest
import time
import logging

import serial

from simple_hdlc import *


class HDLCTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    def test_ok(self):
        s = serial.serial_for_url('loop://', timeout=1)
        h = HDLC(s)
        h.sendFrame(b"hello")
        assert h.readFrame() == b"hello"

    def test_timeout(self):
        s = serial.serial_for_url('loop://', timeout=1)
        h = HDLC(s)
        with self.assertRaises(RuntimeError):
            h.readFrame(timeout=1)

    def test_frames(self):
        h = HDLC(None)
        self.assertTrue(h.current_frame is None)
        self.assertTrue(h.last_frame is None)
        h._readByte(0x7E)
        self.assertTrue(h.current_frame is not None)
        self.assertFalse(h.current_frame.finished)
        h._readByte(0x41)
        h._readByte(0x42)
        h._readByte(0x43)
        # CRC
        h._readByte(0xF5)
        h._readByte(0x08)
        h._readByte(0x7E)
        self.assertTrue(h.current_frame is None)
        self.assertTrue(h.last_frame is not None)
        c = h.last_frame.checkCRC()
        self.assertTrue(c)
        self.assertEqual(h.last_frame.toString(), "ABC")

    def test_wrongframe(self):
        h = HDLC(None)
        self.assertTrue(h.current_frame is None)
        self.assertTrue(h.last_frame is None)
        h._readByte(0x7E)
        self.assertTrue(h.current_frame is not None)
        self.assertFalse(h.current_frame.finished)
        h._readByte(0x41)
        h._readByte(0x42)
        h._readByte(0x43)
        h._readByte(0x08)
        h._readByte(0x7E)
        self.assertTrue(h.last_frame is not None)
        c = h.last_frame.checkCRC()
        self.assertFalse(c)

    def test_reader(self):
        def frame_callback(data):
            frame_callback.called = True
            frame_callback.received = data
        def error_callback(data):
            pass
        s = serial.serial_for_url('loop://', timeout=1)
        h = HDLC(s)
        h.startReader(onFrame=frame_callback, onError=error_callback)
        h.sendFrame(b"hello")
        time.sleep(0.1)
        self.assertTrue(frame_callback.called)
        self.assertEqual(frame_callback.received, "hello")
        h.stopReader()
