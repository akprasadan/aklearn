'''This module builds a class for Poisson regression problems.
We compute the solution by directly maximizing the log-likelihood.
We use an existing software implementation to globally maximize the 
likelihood function: BFGS, available in 
scipy.optimize.minimize(method = 'BFGS)

'''

import numpy as np
from regression import Regression
from evaluation_metrics import evaluate_regression_error
from scipy.optimize import minimize
from scipy.optimize.optimize import _minimize_bfgs

class Poisson(Regression):
    '''
    A class used to represent a Poisson regression model.

    Parameters
    -----------
    features : numpy.ndarray
        Design matrix of explanatory variables.
    output : numpy.ndarray
        Count data output corresponding to feature matrix.
    split_proportion : float
        Proportion of data to use for training; between 0 and 1.
    standardized : bool
        Whether to center/scale the data (train/test done separately).
        True by default.

    Attributes
    ----------
    coefficients : numpy.ndarray
        The coefficients in the Poisson regression model.
    train_predictions : numpy.ndarray
        The predicted output values for the training data.
    test_predictions : numpy.ndarray
        The predicted output values for the test data.
    train_error : float
        The error of model on training data (default is MSE).
    train_error : float
        The error of model on test data (default is MSE).

    Methods
    --------
    fit 
        Fit the Poisson model to training data.
    predict
        Estimate output values on new test data using fitted coefficients.
    '''
    def __init__(self, features, output, split_proportion, 
                 standardized=True):
        super().__init__(features, output, split_proportion, standardized)
        self.coefficients = self.fit()
        self.train_predictions = Poisson.predict(self.train_features, 
                                                self.coefficients)
        self.test_predictions = Poisson.predict(self.test_features, 
                                               self.coefficients)
        self.train_error = evaluate_regression_error(self.train_predictions, 
                                                     self.train_output)
        self.test_error = evaluate_regression_error(self.test_predictions, 
                                                    self.test_output)
    
    @staticmethod
    def loglikelihood(features, counts, coefficient):
        '''Compute empirical log likelihood for each coefficient.

        Parameters
        ----------
        features : numpy.ndarray
            Design matrix of explanatory variables
        counts : numpy.ndarray
            The given response values (integers).
        coefficients : numpy.ndarray
            Vector of coefficients for Poisson regression.
        
        Returns
        -------
        loglikelihood : float
            The value of the log likelihood with given data and coefficient.
        '''

        coeff_matrix = np.tile(coefficient, (features.shape[0], 1))
        dot_prods = np.sum(features * coeff_matrix, axis=1)
        exp_dot_prods = np.exp(dot_prods)
        summands = np.multiply(dot_prods, counts) - exp_dot_prods
        loglikelihood = np.sum(summands)

        return loglikelihood

    @staticmethod
    def mle_finder(features, counts):
        '''
        Find the MLE for a Poisson regression model; return the coefficient.

        Parameters
        ----------
        features : numpy.ndarray
            Design matrix of explanatory variables
        counts : numpy.ndarray
            The given output counts

        Returns
        -------
        mle : float
            The coefficient that solves the Poisson regression problem for 
            the given data.

        Notes
        -----
        We use the BFGS algorithm as implemented in scipy to maximize
        the log-likelihood.
        This requires negating the log likelihood as we use minimization.

        See Also
        --------
        scipy.optimize.minimize
        '''

        def negative_log_likelihood(coefficient):
            ''' The negative log likelihood function that we minimize.
            '''
            value = -Poisson.loglikelihood(features, counts, 
                                            coefficient)
            return value

        dimension = np.ones(counts.shape[1])
        optimum = _minimize_bfgs(negative_log_likelihood, dimension)
        mle = optimum.x  # Obtain argmin
        return mle

    def fit(self):
        '''
        Calculate the coefficient estimate on the training data.
        '''

        coefficients = Poisson.mle_finder(self.train_features, 
                                           self.train_output)

        return coefficients
    
    @staticmethod
    def predict(features, coefficients):
        '''Compute estimated means of Poisson regression.

        Parameters
        ----------
        features : numpy.ndarray
            Design matrix of explanatory variables.
        coefficients : numpy.ndarray
            Vector of coefficients for Poisson regression solution.

        Returns
        -------
        exp_dot_prods : numpy.ndarray
            Predicted mean of Poisson distribution

        Notes
        ------
        In a Poisson model, we assume Y is Poisson, and that
        .. math:: 

            \log \mathbb{E}[Y|x] = \beta^T x. 

        Here we return our estimate of :math: `E[Y|x]`.
        for a test data point x. This quantity reflects the mean 
        (and variance of the) count we might expect of the response,
        conditional on the observed features.

        '''

        coeff_matrix = np.tile(coefficient, (features.shape[0], 1))
        dot_prods = np.sum(features * coeff_matrix, axis=1)
        exp_dot_prods = np.exp(dot_prods)
        
        return exp_dot_prods
    