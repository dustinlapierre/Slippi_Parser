import unittest
from compile_trainset import *
from analytics import *
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

class TestRecovery(unittest.TestCase):
    def test_recovery_state(self):
        mock_data = [
                    32, 999,
                    0, 14, 110.0, -50.0, 1.0, 0.0, 60.0, 4,
                    1, 91, 110.0, 50.0, 1.0, 0.0, 60.0, 4
                    ]
        mock_player1 = player_analytics()
        mock_player1.offstage_state = True
        mock_player1.damaged_state = False
        mock_player2 = player_analytics()
        mock_player2.offstage_state = True
        mock_player2.damaged_state = True

        check_recovery(mock_player1, mock_player2, mock_data)

        self.assertEqual(mock_player1.recovery_state, True)
        self.assertEqual(mock_player2.recovery_state, False)

class TestCommentaryWeight(unittest.TestCase):
    def test_weighting(self):
        commentary_history = [CommentaryNumber.STAGE_CONTROL,
                                CommentaryNumber.NEUTRAL_WINS,
                                CommentaryNumber.BLOCK_SUCCESS]

        mock_player1 = player_analytics()
        mock_player1.recovery_success = 12

        mock_player2 = player_analytics()
        mock_player2.recovery_success = 0

        self.assertEqual(select_commentary_by_weight(mock_player1, mock_player2, commentary_history),
                        CommentaryNumber.RECOVERY)

        commentary_history = [CommentaryNumber.RECOVERY]

        mock_player1.stage_control = 300
        mock_player1.punish_amount = 10
        mock_player1.block_success = 90

        mock_player2.stage_control = 500
        mock_player2.punish_amount = 1
        mock_player2.block_success = 5

        self.assertEqual(select_commentary_by_weight(mock_player1, mock_player2, commentary_history),
                        CommentaryNumber.BLOCK_SUCCESS)

if __name__ == '__main__':
    unittest.main()
