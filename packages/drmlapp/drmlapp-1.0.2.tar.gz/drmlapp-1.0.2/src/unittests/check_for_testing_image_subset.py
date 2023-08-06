import unittest
import sys
import os
import pandas as pd
#sys.path.insert(0,"C:/Users/SUMANTH C/Desktop/DR/src")
#from test import *

class SelectProperImageSubset(unittest.TestCase):

    """
    To check whether the percentage of 0 label images is less than 75%
    """

    def test_percent0(self):

        initial = 0
        final = 100
        labels_path = "E:\\DR\\labels\\train001_filter.csv"
        labels = pd.read_csv(labels_path, header=None)
        labels = labels.values
        labels = labels[initial:final, 1]
        length = len(labels)
        count=0
        for label in labels:
            if label==0:
                count+=1
        count_per = (count/length)*100
        print("No of 0 label images" + str(count_per))
        if(count_per > 75):
            raise Exception("No of test images exceeded by 75% in the subset; Choose a different subset")



if __name__=='__main__':
    unittest.main()