# Building a ML Library From Scratch: Aklearn

My goal for the Summer of 2021 is to upgrade my Python and data science skills, to complement what I have already learned in R. I want to particularly improve my abilities with object oriented programming, numpy, numba, sklearn, and general data analysis/visualization. In addition, I want to explore the 'ecosystem' of software engineering: using version control, good code organization, detailed and effective documentation, and usability (for others).

To do so, I will create a unified framework (similar to Tidymodels in R or Sklearn in Python) to perform ML in Python. I will begin with base classes for Classification, Regression, Clustering, for instance, from which I will derive classes for each algorithm of interest. I will provide functionality for train/test and cross-validation splitting, model tuning, model evaluation (with a variety of metrics), and automatically generated plots.

You can find all the documentation [here](https://akprasadan.github.io/Summer2021ML/index.html), produced using Sphinx and Read the Docs.

## Progress So Far (in both workflow and explicit code)

- Consistent use of Git/Github for version control
- General class for Regression, and child classes including Linear, Poisson, and KNN regression.
- General class for Classification, and child classes including Logistic, KNN classification
- Train/test splitting functionality
- Autogenerated documentation: [here](https://akprasadan.github.io/Summer2021ML/index.html)


## TODO (in the next 2 weeks)

- Cross-validation, bootstrapping functionality
- Abstract tuning class and incorporation into child classes
- Linear/quadratic discriminant analysis
- LASSO? Other penalized estimators

## Eventually:
- Classification trees, bagging, random forests
- Boosting
- Support vector machines
- Stacking functionality

## License
[MIT](https://choosealicense.com/licenses/mit/)

![](https://github.com/akprasadan/aklearn/workflows/Project%20Tests/badge.svg)
