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

    def test_CheckEagle(self):
        from Swoop.tools.CheckEagle import main

        files = ["inputs/Components.lbr",
                "inputs/ComponentsEagle9.lbr",
                "inputs/Quadcopter.koala.sch",
                "inputs/ShapelyTextTest.brd",
                "inputs/Trinket_Pro_default_SMD_parts_power_breakout.koala.sch",
                "inputs/Xperimental_Trinket_Pro_small_parts_power_breakout.picked.brd",
                "inputs/Xperimental_Trinket_Pro_small_parts_power_breakout.picked.eagle9.brd",
                "inputs/Xperimental_Trinket_Pro_small_parts_power_breakout.picked.eagle9.sch",
                "inputs/Xperimental_Trinket_Pro_small_parts_power_breakout.picked.sch",
                "inputs/cleanup_test01.brd",
                "inputs/cleanup_test01.lbr",
                "inputs/cleanup_test01.sch",
                "inputs/curve_test.brd",
                "inputs/eagle9-minimal.brd",
                "inputs/eagle9-minimal.sch",
                "inputs/fp_bbox.brd",
                "inputs/geo_test.sch",
                "inputs/loud-flashy-driver.postroute.brd",
                "inputs/shapeTest1.brd",
                "inputs/shapeTest1.lbr",
                "inputs/shapeTest1.sch",
                "inputs/shapeTest2.brd",
                "inputs/shapeTest2.sch",
                "inputs/shapeTest3.brd",
                "inputs/shapeTest5.brd",
                "inputs/test01.sch",
                "inputs/test02.sch",
                "inputs/test03.sch",
                "inputs/test04.sch",
                "inputs/test05.sch",
                "inputs/test06.sch",
                "inputs/test_query.brd",
                "inputs/test_query.sch",
                "inputs/test_saving.brd",
                "inputs/test_saving.sch",
        ]
        for i in files:
            r = main(["--internal-check", "--file", os.path.join(self.curdir, i)])
            self.assertTrue(r == 0)

        
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

