import unittest
import sys
sys.path.insert(0,"C:/Users/SUMANTH C/Desktop/DR/src")
from features_input import *

class NumberofTestImagesTest(unittest.TestCase):

    def test_checktestimages(self):
        img_path = "E:\\DR\\datasets\\filtered_dataset\\train001\\"
        initial = 0
        final = 1
        self.assertGreater(final, initial)
        features_input = VGG16Conv(img_path, initial, final)
        print(features_input.shape)



if __name__=='__main__':
    unittest.main()

