import unittest

from Helpers.TapHelper import get_next_tap
from Enums.Replays.StandardKeys import StandardKeys as Key

NONE = Key.none
K1 = Key.K1
K2 = Key.K2
K1N2 = Key.K1 + Key.K2

class Test(unittest.TestCase):

    def test_get_next_tap(self):
        tap_seq_0 = [NONE,NONE,NONE,K1,K1,K1,K1,K1N2,K1N2,K2,NONE,K1,K2,K1N2,K1,K1,K1N2,K1N2,K2,NONE,NONE]

        ret_val = get_next_tap(tap_seq_0, idx=0)
        self.assertEqual(ret_val, [3, 9, 7])

        ret_val = get_next_tap(tap_seq_0, ret_val[2])
        self.assertEqual(ret_val, [7, 9, 10])

        ret_val = get_next_tap(tap_seq_0, ret_val[2])
        self.assertEqual(ret_val, [11, 18, 12])

        ret_val = get_next_tap(tap_seq_0, ret_val[2])
        self.assertEqual(ret_val, [12, 18, 13])

        ret_val = get_next_tap(tap_seq_0, ret_val[2])
        self.assertEqual(ret_val, [13, 18, 16])

        ret_val = get_next_tap(tap_seq_0, ret_val[2])
        self.assertEqual(ret_val, [16, 18, 19])

        ret_val = get_next_tap(tap_seq_0, ret_val[2])
        self.assertIsNone(ret_val)

if __name__ == '__main__':
    unittest.main()