import unittest
from compile_trainset import *
import numpy as np
import os

class TestCompileTrainset(unittest.TestCase):
    def test_data(self):
        #test if data captured properly (on edge cases)
        set_size = len(os.listdir('training_set/data'))
        data = compile_data()
        self.assertEqual(data[0][0], [0, 20, -58.18000030517578, 9.999999747378752, 1.0, 0.0, 60.0, 4])
        self.assertEqual(data[0][99], [0, 20, -49.3912467956543, 9.999999747378752, -1.0, 0.0, 60.0, 4])
        self.assertEqual(data[set_size-1][0], [0, 14, -60.0, 9.999999747378752, 1.0, 0.0, 60.0, 4])
        self.assertEqual(data[set_size-1][99], [0, 14, -60.0, 9.999999747378752, 1.0, 0.0, 60.0, 4])

        #test if shape is correct
        data = np.array(data, dtype=np.float32)
        self.assertEqual(data.shape, (set_size, 100, 8))

if __name__ == '__main__':
    unittest.main()
