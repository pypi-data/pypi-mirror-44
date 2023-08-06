import unittest
import Swoop
import Swoop.tools
import os
import re
import math
from lxml import etree as ET

class TestSwoop(unittest.TestCase):

    def setUp(self):
        self.curdir = os.path.dirname(os.path.realpath(__file__))
        self.tmpdir = os.path.join(self.curdir, "temp")
        if not os.path.exists(self.tmpdir):
            os.makedirs(self.tmpdir)

        self.me = os.path.dirname(os.path.realpath(__file__))
        self.sch_file = self.me + "/inputs/Xperimental_Trinket_Pro_small_parts_power_breakout.picked.eagle9.sch"
        self.sch = Swoop.EagleFile.from_file(self.sch_file, bestEffort=False);
        self.brd_file = self.me + "/inputs/Xperimental_Trinket_Pro_small_parts_power_breakout.picked.eagle9.brd"
        self.brd = Swoop.EagleFile.from_file(self.brd_file, bestEffort=False)
        self.lbr_file = self.me + "/inputs/ComponentsEagle9.lbr"
        self.lbr = Swoop.EagleFile.from_file(self.lbr_file, bestEffort=False)

    def test_Load(self):
        pass

    def test_Write(self):
        import io
        output = io.StringIO()
        self.sch.write(output)
        try:
            self.sch.write(output)
        except e:
            self.assertTrue(False, "Schematic write to string failed")
            raise e

        self.brd.write(output)
        try:
            self.brd.write(output)
        except e:
            self.assertTrue(False, "Board write to string failed")
            raise e

        self.lbr.write(output)
        try:
            self.lbr.write(output)
        except e:
            self.assertTrue(False, "Library write to string failed")
            raise e

    def test_Clone(self):
        a = Swoop.EagleFile.from_file(os.path.join(self.me, "inputs/Trinket_Pro_default_SMD_parts_power_breakout.koala.sch"))
        a.clone()
        a.write("foo.sch")

        for a in [self.brd, self.sch, self.lbr]:
            b = a.clone()
            b.write("/dev/null")
        
    def tearDown(self):
        # Remove self.tmpdir
        try:
            for root, dirs, files in os.walk(self.tmpdir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.tmpdir)
        except:
            pass

