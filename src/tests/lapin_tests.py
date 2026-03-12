import unittest

import numpy as np

from experiments.lapin.lapin import lapin


class Test(unittest.TestCase):

    def test_lapin_symmetric_normalized_laplacian(self):
        W = np.matrix([[1, 0, 1], [0, 3, 0], [1, 0, 9]])
        W_transformed = lapin(W, laplacian_variant='symmetric_normalized_laplacian')
        print(W_transformed)
        self.assertTrue(W_transformed.shape == W.shape)

    def test_lapin_random_walk_normalized_laplacian(self):
        W = np.matrix([[1, 0, 1], [0, 3, 0], [1, 0, 9]])
        W_transformed = lapin(W, laplacian_variant='random_walk_normalized_laplacian')
        print(W_transformed)
        self.assertTrue(W_transformed.shape == W.shape)

    def test_lapin_unnormalized_laplacian(self):
        W = np.matrix([[1, 0, 1], [0, 3, 0], [1, 0, 9]])
        W_transformed = lapin(W, laplacian_variant='unnormalized_laplacian')
        print(W_transformed)

    def test_lapin_invalid_laplacian_variant(self):
        W = np.matrix([[1, 0, 1], [0, 3, 0], [1, 0, 9]])
        self.assertRaises(ValueError, lapin, W, laplacian_variant='invalid_variant')


if __name__ == "__main__":
    unittest.main()
