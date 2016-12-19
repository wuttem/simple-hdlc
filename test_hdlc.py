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
