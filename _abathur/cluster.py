import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
import pandas as pd
from collections import defaultdict


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

    def _determine_max_k(self, feat_array):
        """
        Determine the what is the maximum number of clusters to consider.
        [1] Kanti Mardia et al. (1979). Multivariate Analysis. Academic Press.
        """

        return int(round(np.sqrt(feat_array.shape[0] / 2.0)))

    def _determine_k(self, feat_array, max_cluster=0, multi_run=3):
        """
        Use the jump method to find ideal k by using an information theoretic
        approach.

        In order to find a good jump, we run multiple times and the the lower
        bound and use it to compute the best k to choose from.

        Ref:
        ----

        [1] Catherine A. Sugar and Gareth M. James (2003). "Finding the number
        of clusters in a data set: An information theoretic approach".  Journal
        of the American Statistical Association 98 (January): 750-765.
        """
        def _get_jump(feat_array, max_cluster):
            if max_cluster < 2:
                max_cluster = self._determine_max_k(feat_array)
            whitened = whiten(feat_array)
            # first obtain the covariance matrix of the feature array
            gamma = np.cov(whitened.T)
            num_dim = whitened.shape[1]
            jump = {}
            distortions_dict = {0: 1}
            power_fact = -num_dim / 2.0
            # Run k mean for all possible number of clusters
            for k in xrange(1, max_cluster + 1):
                codebook, _ = kmeans(whitened, k, iter=self.iter)
                code, _ = vq(whitened, codebook)

                clusters_dict = self._segment_to_clusters(whitened, code)
                mahalanobis_dist_list = []
                for cid, cvals in clusters_dict.iteritems():
                    centroid = codebook[cid]
                    cluster_mahalanobis_dist = map(
                        lambda x: self._sq_mahalanobis(x, centroid, gamma),
                        clusters_dict[cid].values)
                    mahalanobis_dist_list.extend(cluster_mahalanobis_dist)
                this_distortion = np.mean(mahalanobis_dist_list) / num_dim
                distortions_dict[k] = this_distortion ** power_fact

            for k in xrange(1, max_cluster + 1):
                jump[k] = distortions_dict[k] - distortions_dict[k - 1]

            return jump

        jump_list = []
        for i in xrange(multi_run):
            jump_list.append(_get_jump(feat_array, max_cluster))

        jump_combined = defaultdict(list)
        for jump_dict in jump_list:
            for idx, val in jump_dict.iteritems():
                jump_combined[idx].append(val)
        jump_final = dict([(i, min(v)) for i, v in jump_combined.iteritems()])

        best_k = max(jump_final, key=jump_final.get)

        print "Chose {} as best number of clusters.".format(best_k)

        return best_k

    def _segment_to_clusters(self, feat_array, code):
        feat_df = pd.DataFrame(feat_array)
        cluster_labels = pd.Series(code)

        segmented = {}
        for c in cluster_labels.unique():
            segmented[c] = feat_df[cluster_labels == c]

        return segmented

    def _sq_mahalanobis(self, x, center, cov_matrix):
        """
        Returns the squared mahalanobis distance
        """
        x_center_diff = x - center
        return x_center_diff.dot(np.linalg.inv(cov_matrix)).dot(
            x_center_diff.T)

    def _get_cluster(self, feat_array, k):
        # Normalise the feature array
        whitened = whiten(feat_array)

        codebook, _ = kmeans(whitened, k, iter=self.iter)
        code, _ = vq(whitened, codebook)
        return code
