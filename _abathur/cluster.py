import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten


class Clusterer(object):

    def __init__(self, input_filename, output_filename, ignore):
        self._input_filename = input_filename
        self._output_filename = output_filename
        self._ignore = ignore

    def perform_clustering(self):
        # First read the input csv in as numpy array
        feat_array = np.loadtxt(
            self._input_filename, delimiter=",", skiprows=1)  # skip header

        # Then determine k
        k = self._determine_k(feat_array)

        # Find and return the kmean to output
        code = self._get_cluster(feat_array, k)

        print code

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

        codebook, _ = kmeans(whitened, k)
        code, _ = vq(whitened, codebook)
        return code
