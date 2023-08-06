import unittest
import sys
import os
sys.path.insert(0,"C:/Users/SUMANTH C/Desktop/DR/src")
from test import *

class CheckOverfitting(unittest.TestCase):

    def test_overfitting(self):
        img_path = "E:\\DR\\datasets\\filtered_dataset\\train001\\"
        initial = 0
        final = 100
        model_path = "E:\\DR\\trained_models\\oversample_model_train005_0_1427_512.h5"
        test_csv_path = "E:\\DR\\labels\\train001_filter.csv"
        stats = 1
        cf= test(img_path, initial, final, model_path, test_csv_path,stats)
        print(cf)
        #cf = [[100,0,0,0,0],[8,0,0,0,0],[6,0,0,0,0],[4,0,0,0,0],[2,0,0,0,0]]
        if((cf[1][0]!=0 and cf[1][1]==0 and cf[1][2]==0 and cf[1][3]==0 and cf[1][4]==0) and
                (cf[2][0]!=0 and cf[2][1]==0 and cf[2][2]==0 and cf[2][3]==0 and cf[2][4]==0) and
                    (cf[3][0]!=0 and cf[3][1]==0 and cf[3][2]==0 and cf[3][3]==0 and cf[3][4]==0) and
                        (cf[4][0]!=0 and cf[4][1]==0 and cf[4][2]==0 and cf[4][3]==0 and cf[4][4]==0)):
            raise Exception("Overfitting has Occured")


if __name__=='__main__':
    unittest.main()