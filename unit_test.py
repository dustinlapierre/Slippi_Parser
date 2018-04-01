import unittest
from compile_trainset import *
from analytics import check_shield_pressure
import numpy as np
import os

class TestCompileTrainset(unittest.TestCase):
    def test_data(self):
        #test if data captured properly (on edge cases)
        set_size = len(os.listdir('training_set/data'))
        data = compile_data()
        self.assertEqual(data[0][0], [-0.9, -0.20679999999999998, 0.0, 1.0])
        self.assertEqual(data[0][99], [-0.9, -0.08055999999999996, 0.0, 1.0])
        self.assertEqual(data[set_size-1][0], [-0.9, -0.24, 0.0, 1.0])
        self.assertEqual(data[set_size-1][99], [-0.9, 0.0722799999999999, 0.0, -1.0])

        #test if shape is correct
        data = np.array(data, dtype=np.float32)
        self.assertEqual(data.shape, (set_size, 100, 4))

class TestShieldPressure(unittest.TestCase):
    def test_pressure(self):
        #test if mock gameplay data satisfies shield pressure criteria
        #data: [stage, frame num, (player index, action, x, y, direction, percent, shield, stocks) x 2]
        mock_data = [
                    32, 999,
                    0, 14, 12.0, 0.0, 1.0, 0.0, 60.0, 4,
                    1, 179, 18.0, 0.0, -1.0, 0.0, 24.5, 4
                    ]
        self.assertEqual(check_shield_pressure(mock_data), (True, False))
        mock_data = [
                    32, 999,
                    0, 179, -40.0, 0.0, -1.0, 0.0, 15.0, 4,
                    1, 14, -35.0, 0.0, -1.0, 0.0, 60.0, 4
                    ]
        self.assertEqual(check_shield_pressure(mock_data), (False, True))
        mock_data = [
                    32, 999,
                    0, 14, 0.0, 0.0, 1.0, 0.0, 45.0, 4,
                    1, 14, -12.0, 0.0, 1.0, 0.0, 53.5, 4
                    ]
        self.assertEqual(check_shield_pressure(mock_data), (False, False))

if __name__ == '__main__':
    unittest.main()
