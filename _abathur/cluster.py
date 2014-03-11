import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
import pandas as pd


class Clusterer(object):

    def __init__(self, input_filename, output_filename, ignore):
        self._input_filename = input_filename
        self._output_filename = output_filename
        self._ignore = ignore
        # unless explicitly set, the default number of kmeans to be run is 10
        self.iter = 10

    def perform_clustering(self):
        df = pd.read_csv(self._input_filename)
        feature_cols = list(df.columns.values)
        for non_feat_col in self._ignore:
            feature_cols.remove(non_feat_col)
        feat_array = df[feature_cols].values

        # Then determine k
        k = self._determine_k(feat_array)

        # Find and return the kmean to output
        code = self._get_cluster(feat_array, k)

        with open(self._output_filename, "wb") as output_file:
            output_file.writelines([str(i) + "\n" for i in code])

    def _determine_k(self, feat_array):
        """
        The placeholder for better algorithm to determine k, for now we just
        use k = sqrt(n/2) [1] as a naive starting point.
        [1] Kanti Mardia et al. (1979). Multivariate Analysis. Academic Press.
        """

        return round(np.sqrt(feat_array.shape[0] / 2.0))

    def _get_cluster(self, feat_array, k):
        # Normalise the feature array
        whitened = whiten(feat_array)

        codebook, _ = kmeans(whitened, k, iter=self.iter)
        code, _ = vq(whitened, codebook)
        return code
