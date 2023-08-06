"""
PyUnit test module for PythonCA

Unit test case definition and runner.
"""
import random
import unittest
import os
import ca
class TestEZCA(unittest.TestCase):
    def setUp(self):
        """
        setup routine for each test cases.
        make sure that caRepeater and EPICS database is running
        """
        pass

    def tearDown(self):
        """
        Clean up routine for each TestCases
        """
        pass

    def testGet(self):
        self.assert_(ca.Get("fred"))

    def testPut(self):
        self.assert_(ca.Put("fred",0.2))

    def testPut_Array(self):
        l=random.sample(xrange(10000),100)
        ca.Put_Array("albert",l)
        self.assertEquals(ca.Get("albert")[:100],l)

    def testGetNoChanne(self):
        self.assertRaises(ca.ECA_BADTYPE,ca.Get,("xxx",))

    def testSyncGroup(self):
        sg=ca.SyncGroup()
        sg.add((ca.channel("fred"),ca.channel("jane")))
        ca.flush()
        sg.add("jane")
        sg.add("freddy")
        sg.GetAll(tmo=1.0)
        print [(ch.name, ca.TS2Ascii(ch.ts), ch.val) for ch in sg.chs]
        del sg
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEZCA)
    unittest.TextTestRunner(verbosity=2).run(suite)
