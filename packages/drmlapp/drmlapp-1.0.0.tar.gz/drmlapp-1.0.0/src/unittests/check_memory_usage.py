import unittest
import sys
import os
import psutil
sys.path.insert(0,"C:/Users/SUMANTH C/Desktop/DR/src")
from features_input import *

class MemoryUsageCheck(unittest.TestCase):

    def test_memoryusage(self):
        img_path = "E:\\DR\\datasets\\filtered_dataset\\train001\\"
        initial = 0
        final = 4

        features_input = VGG16Conv(img_path, initial, final)
        print(psutil.virtual_memory())
        mem_usage = psutil.virtual_memory()[2]
        print('memory % used:', str(mem_usage))
        print(features_input.shape)
        self.assertGreater( 80 , mem_usage)

if __name__=='__main__':
    unittest.main()
