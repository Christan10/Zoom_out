from zoom_out import *
import unittest

class TestHMat(unittest.TestCase):

    def setUp(self):
        pass

    def test_find_next_max_freq(self):
        k=4
        TestHmat = []
        TestHmat.append(HRow(1, 1))
        TestHmat.append(HRow(2, 4))
        TestHmat.append(HRow(3, 1))
        TestHmat.append(HRow(7, 3))
        TestHmat.append(HRow(5, 3))
        hmat = HMat()
        hmat.Hmat = TestHmat
        result = hmat.find_next_max_freq_rows(k, 1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 3)



if __name__ =='__main__':
	unittest.main()