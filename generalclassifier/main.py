import numpy as np
from numba import jit

class SupervisedAlgorithm:

    def __init__(self, features, output, split_proportion):
        self.features = np.array(features)
        self.output = np.array(output)
        self.split_proportion = split_proportion
        self.sample_size = self.features.shape[0]
        self.train_size = np.ceil(self.sample_size * split_proportion)
        # https://stackoverflow.com/a/14262743
        self.train_rows = np.random.choice(self.train_size.shape[0], self.train_size, replace=False)
        self.test_rows = np.setdiff1d(np.arange(self.sample_size), self.train_rows)
        self.train_features = self.features[self.train_rows]
        self.test_features = self.features[self.test_rows]
        self.train_output = self.output[self.train_rows]
        self.test_output = self.output[self.test_rows]
    
    def fit_to(self, input, output):
        pass
    
    @staticmethod
    def scale_and_center(feature_matrix):
        '''Center and scale the feature matrix.'''

        n_rows, n_cols = feature_matrix.shape
        for column in range(n_cols):
            feature_matrix[:, column] = (feature_matrix[:, column] - np.mean(feature_matrix[:, column])*np.ones(n_rows)) \
                / np.std(feature_matrix[:, column])
        return feature_matrix


class Classification(SupervisedAlgorithm):

    def __init__(self, features, output, split_proportion, number_labels = None):
        super().__init__(features, output, split_proportion)
        if number_labels is None: # Default procedure is to assume all labels appear in the output; otherwise, specify manually
            self.number_labels = len(np.unique(output)) 
        else: 
            self.number_labels = number_labels
        self.labels = np.arange()

    

class Regression(SupervisedAlgorithm):

    def __init__(self, features, output, split_proportion, number_labels = None):
        super().__init__(features, output, split_proportion)

    @staticmethod