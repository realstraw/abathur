import unittest
import numpy as np
import sys
import os
import shutil
import filecmp

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from _abathur.cluster import Clusterer


class TestClustererFunctions(unittest.TestCase):

    TMP_DIR = "/tmp/abathur_unittest"

    def setUp(self):
        tmp_dir = self.__class__.TMP_DIR

        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir)

    def tearDown(self):
        tmp_dir = self.__class__.TMP_DIR
        shutil.rmtree(tmp_dir)

    def test_determine_max_k(self):
        test_dir_name = os.path.dirname(__file__)
        feat_array_fn = os.path.join(
            test_dir_name, "data", "feature_array.csv")
        feat_array = np.loadtxt(feat_array_fn, delimiter=",", skiprows=1)

        clusterer = Clusterer("_", "_", [])
        k = clusterer._determine_max_k(feat_array)
        self.assertEqual(k, 2)

    def test_perform_clustering(self):
        test_dir_name = os.path.dirname(__file__)
        feat_array_fn = os.path.join(
            test_dir_name, "data", "feature_array.csv")

        tmp_dir = self.__class__.TMP_DIR
        output_fn = os.path.join(tmp_dir, "code.txt")

        clusterer = Clusterer(feat_array_fn, output_fn, [])
        clusterer.iter = 100
        clusterer.perform_clustering()

        sample_output_filename = os.path.join(
            test_dir_name, "data", "sample_cluster_code.txt")
        sample_inv_output_filename = os.path.join(
            test_dir_name, "data", "sample_cluster_code_inv.txt")

        same_as_sample = filecmp.cmp(output_fn, sample_output_filename)
        same_as_inv = filecmp.cmp(output_fn, sample_inv_output_filename)
        self.assertTrue(same_as_sample or same_as_inv)

        # Now test the data set with non feat cols
        feat_array_fn = os.path.join(
            test_dir_name, "data", "feature_array_with_non_feat_cols.csv")
        clusterer = Clusterer(feat_array_fn, output_fn, ["id", "param"])
        clusterer.iter = 100
        clusterer.perform_clustering()

        same_as_sample = filecmp.cmp(output_fn, sample_output_filename)
        same_as_inv = filecmp.cmp(output_fn, sample_inv_output_filename)
        self.assertTrue(same_as_sample or same_as_inv)


if __name__ == "__main__":
    unittest.main()
