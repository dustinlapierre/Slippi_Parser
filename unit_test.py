import unittest
from compile_trainset import *
import numpy as np
import os

class TestCompileTrainset(unittest.TestCase):
    def test_data(self):
        #test if data captured properly (on edge cases)
        set_size = len(os.listdir('training_set/data'))
        data = compile_data()
        self.assertEqual(data[0][0], [-0.9, -0.20679999999999998, 0.0, 1.0])
        self.assertEqual(data[0][99], [-0.9, -0.08055999999999996, 0.0, 1.0])
        self.assertEqual(data[set_size-1][0], [-0.9, -0.08628000000000002, 0.0, 1.0])
        self.assertEqual(data[set_size-1][99], [-0.9, 0.016119999999999912, 0.0, -1.0])

        #test if shape is correct
        data = np.array(data, dtype=np.float32)
        self.assertEqual(data.shape, (set_size, 100, 4))

class TestShieldPressure(unittest.TestCase):
    def test_pressure(self):
        #test if mock recovery data fits
        self.assertEqual(data.shape, (set_size, 100, 4))

if __name__ == '__main__':
    unittest.main()
