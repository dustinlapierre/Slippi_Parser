import unittest
from compile_trainset import *
from analytics import get_matchup_score
from general import flatten
import numpy as np
import os

class TestCompileTrainset(unittest.TestCase):
    def test_data(self):
        #test if data captured properly (on edge cases)
        set_size = len(os.listdir('training_set/data'))
        data = compile_data()
        self.assertEqual(data[0][0], [-0.9, -0.20679999999999998, 0.0, 1.0])
        self.assertEqual(data[0][99], [-0.9, -0.08055999999999996, 0.0, 1.0])
        self.assertEqual(data[set_size-1][0], [-0.9, 0.22496000000000005, 0.0, -1.0])
        self.assertEqual(data[set_size-1][99], [-0.9299999999999999, 0.10831999999999997, 0.0, 1.0])

        #test if shape is correct
        data = np.array(data, dtype=np.float32)
        self.assertEqual(data.shape, (set_size, 100, 4))

class TestMatchupChart(unittest.TestCase):
    def test_matchups(self):
        self.assertEqual(get_matchup_score("Fox", "Fox"), "This matchup is fairly even.")
        self.assertEqual(get_matchup_score("Captain Falcon", "Falco"), "This matchup is extremely bad for Captain Falcon.")
        self.assertEqual(get_matchup_score("Bowser", "Peach"), "This is a matchup we don't see often!")

class TestNormalization(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(flatten(5.0, 0.0, 10.0), 0.5)

if __name__ == '__main__':
    unittest.main()
