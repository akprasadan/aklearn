'''This module builds a class for k-nearest neighbor classification.
'''

import numpy as np
from numpy.lib.shape_base import split
from src.classification.classification import Classification
from src.helperfunctions.evaluation_metrics import evaluate_accuracy, confusion_matrix

class QDA(Classification):
    '''
    A class used to represent a quadratic discriminant analysis classifier.
    We only list non-inherited attributes. We include regression
    functionality as well.

    Parameters
    -----------
    features : numpy.ndarray
        Design matrix of explanatory variables.
    output : numpy.ndarray
        Labels of data corresponding to feature matrix.
    split_proportion : float
        Proportion of data to use for training; between 0 and 1.
    number_labels : int
        The number of labels present in the data.
    standardized : bool
        Whether to center/scale the data (train/test done separately).
        True by default.
    
    Attributes
    ----------
    train_prediction : numpy.ndarray
        The labels predicted for the given test data (for classification).
    test_predictions : numpy.ndarray
        The labels predicted for the given test data (for classification).
    train_accuracy : float
        The accuracy of the classifier evaluated on test data
    test_accuracy : float
        The accuracy of the classifier evaluated on test data 
        (for classification).
    train_confusion : numpy.ndarray
        A confusion matrix of the classifier evaluated on training data 
        (for classification).
    test_confusion : numpy.ndarray
        A confusion matrix of the classifier evaluated on test data 
        (for classification).

    See Also
    ---------
    lda.LDA : Use the more restrictive linear discriminant analysis
    '''

    def __init__(self, features, output, split_proportion=0.75,
                 number_labels=None, standardized=True):
        super().__init__(features, output, split_proportion, number_labels, 
                         standardized)

        self.train_predictions = self.predict_many(self.train_features)
        self.test_predictions = self.predict_many(self.test_features)
        self.train_accuracy = evaluate_accuracy(self.train_predictions, 
                                            self.train_output)
        self.train_confusion = confusion_matrix(self.number_labels, 
                                            self.train_predictions, 
                                            self.train_output)
        self.test_accuracy = evaluate_accuracy(self.test_predictions, 
                                            self.test_output)
        self.test_confusion = confusion_matrix(self.number_labels, 
                                            self.test_predictions, 
                                            self.test_output)
    
    @staticmethod
    def prior(output, k):
        ''' Count the empirical proportion of labels of class k among output data.
        
        Parameters
        -----------
        output : numpy.ndarray
            The labels corresponding to some dataset
        k : int 
            The class label we are interested in

        Returns
        --------
        proportion : float
            The fraction of class k observations
        '''

        frequency = np.count_nonzero(output == k)
        proportion = frequency / output.shape[0]

        return proportion
          
    @staticmethod
    def class_covariance(features_subset):
        ''' Calculate a covariance matrix for a mono-labeled feature array.
        
        Parameters
        -----------
        features_subset : numpy.ndarray
            The design matrix of explanatory variables.

        Returns
        --------
        class_cov : numpy.ndarray
            The class-specific covariance matrix for QDA.
        '''

        sample_size, dim = features_subset.shape
        class_mean = np.mean(features_subset, axis=0)
        centered_features_subset = features_subset - class_mean
        unscaled_class_cov = centered_features_subset.T @ centered_features_subset

        if sample_size == 1:
            class_cov = 1/(sample_size) * unscaled_class_cov
        else: 
            class_cov = 1/(sample_size - 1) * unscaled_class_cov
        return class_cov

    def discriminant(self, point, k):
        ''' Evaluate the kth quadratic discriminant function at a point.

        Parameters
        -----------
        point : numpy.ndarray
            The point to evaluate at
        k : int
            The class label of interest

        Returns
        --------
        discrim : float
            The value of the discriminant function at this point.
        '''
        feature_subset = self.train_features[self.train_output == k]
        class_cov = QDA.class_covariance(feature_subset)
        mean_term = np.mean(feature_subset, axis = 0)
        log_det_term = -0.5*(np.log(np.linalg.det(class_cov)))
        inv_term = np.linalg.inv(class_cov)
        prior_term = np.log(QDA.prior(self.train_output, k))
        quadratic_term = -0.5*(point - mean_term).T @ inv_term @ (point - mean_term)

        discrim = log_det_term + quadratic_term + prior_term

        return discrim
  
    def predict_one(self, point):
        '''Predict the label of a test point given a trained model.

        Parameters
        -----------
        point : numpy.ndarray
            The test datapoint we wish to classify.

        Returns
        --------
        label : int
            The predicted class of the point.
        '''

        discrims = np.array([self.discriminant(point, k) for k in range(self.number_labels)])
        label = np.where(discrims == np.max(discrims))[0][0]
        return label
    
    def predict_many(self, points):
        '''Predict the label of a matrix of test points given a trained model.

        Parameters
        -----------
        points : numpy.ndarray
            The test datapoints we wish to classify.

        Returns
        --------
        label : int
            The predicted classes of the points.
        '''
        try:
            labels = np.apply_along_axis(self.predict_one, 1, points).astype(np.int8)
            return labels
        except:
            return 



